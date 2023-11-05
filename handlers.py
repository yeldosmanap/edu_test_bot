from aiogram import types, F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from buttons import backButtonMenuKeyboard, subjects, keyboard
from main import connection_pool


class Form(StatesGroup):
    START_TEST = State()
    SUBJECT = State()
    QUESTIONS = State()
    ANSWER = State()


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    print('Start handler', message.from_user.username)
    await state.clear()
    username = message.from_user.username
    conn = connection_pool.getconn()
    cur = conn.cursor()

    try:
        cur.execute("SELECT u.username FROM users u WHERE u.username = %s;", (username,))
        usernameInDb = cur.fetchone()

        if usernameInDb is not None:
            await message.answer(f'Welcome back @{username}!', reply_markup=keyboard)
        else:
            cur.execute("INSERT INTO users (username, date_signed_in) VALUES (%s, CURRENT_TIMESTAMP);", (username,))
            conn.commit()
            await message.answer(f'Welcome @{username} to our Telegram Bot for education!', reply_markup=keyboard)
    finally:
        cur.close()
        connection_pool.putconn(conn)

    # Get statistics for the user
    statistics = get_statistics(username)

    # Format and send the statistics
    statistics_message = "Statistics:\n\n"
    if not statistics:
        statistics_message += "No correct answers gotten yet."
    else:
        for subject in statistics:
            subject_name = subject['subject_name']
            correct_answers = subject['correct_answers']
            statistics_message += f"Subject: {subject_name}\nCorrect Answers: {correct_answers}\n\n"

    await message.answer(statistics_message)


@router.message(StateFilter(None))
async def select(message: types.Message, state: FSMContext) -> None:
    if message.text == 'Help':
        print('Help button pressed')
        await message.answer(
            '''This bot is designed to help you learn and test your knowledge in different subjects. To get started,
            simply select the subject you would like to study or test from the menu below.''',
            reply_markup=backButtonMenuKeyboard)
    elif message.text == 'Start test':
        print('Start test button pressed', message.from_user.username)
        await message.answer('Please select the subject you would like to test:', reply_markup=subjects)
        await state.set_state(Form.START_TEST)
        print('State set to START_TEST')


@router.message(Form.START_TEST)
async def start_test_handler(message: types.Message, state: FSMContext) -> None:
    print('Start test handler', message.from_user.username)
    await state.update_data(SUBJECT=message.text)
    await message.answer(f"'Let's start a quiz on subject {message.text}!")
    await state.set_state(Form.SUBJECT)


@router.message(Form.SUBJECT)
async def process_subject(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    print(f'Process subject {user_message}', message.from_user.username)
    await state.update_data(SUBJECT=user_message)
    await message.answer(f'You have selected {user_message}')
    await message.answer('Please enter the number of questions you want to answer:')
    await state.set_state(Form.QUESTIONS)
    # Assuming you have a function to get questions based on the subject
    questions = get_questions_for_subject_by_username(user_message, message.from_user.username)
    if not questions:
        await message.answer('No questions available for this subject.')
        return

    # Set the user's state to TestState.questions
    await state.set_state(Form.QUESTIONS)


@router.message(Form.QUESTIONS)
async def process_questions(message: types.Message, state: FSMContext) -> None:
    # Get the user's state
    user_data = await state.get_data()
    subject = user_data.get('SUBJECT')

    # Get the number of questions
    try:
        num_questions = int(message.text)
        if num_questions <= 0:
            raise ValueError()
    except ValueError:
        await message.answer('Please enter a valid positive number.')
        return

    # Get questions for the selected subject
    questions = get_questions_for_subject_by_username(subject, message.from_user.username)
    print(questions)

    await state.update_data(num_questions=num_questions, questions=questions)

    # Check if there are enough questions
    if len(questions) < num_questions:
        await message.answer('Not enough questions available for this subject.')
        return

    # Reset the state to START_TEST
    await state.set_state(Form.START_TEST)

    # Get the first question
    first_question = questions[0]
    question_text = first_question['question_text']
    level = first_question['level_id']
    subject_name = first_question['subject_name']

    # Save question_id, level_id, and answer_text in user_data
    await state.update_data(
        question_id=first_question['question_id'],
        level_id=level,
        subject_name=subject_name,
        answer_text=first_question['answer_text']
    )

    # Show the description of the question and level type
    await message.answer(f'Question: {question_text}\nLevel: {level}')
    # Update the user's state to 'answer'
    await state.set_state(Form.ANSWER)


@router.message(Form.ANSWER)
async def process_answer(message: types.Message, state: FSMContext) -> None:
    # Get the user's state
    user_data = await state.get_data()
    question_id = user_data.get('question_id')
    username = message.from_user.username
    level_id = user_data.get('level_id')
    subject_name = user_data.get('subject_name')
    # Get the correct answer for the current question
    correct_answer = user_data.get('answer_text')

    # Get the user's answer
    user_answer = message.text

    if user_answer == correct_answer:
        await message.answer('Congratulations! Your answer is correct.')
        # Store the user's answer in the database
        store_user_answer(question_id, username, level_id, subject_name)
    else:
        await message.answer(f'Your answer is not correct. The correct answer is: {correct_answer}')

    # # Get the next question
    # next_question = get_next_question(question_id)
    #
    # if next_question:
    #     # Show the next question
    #     question_text = next_question['question_text']
    #     level = next_question['level_id']
    #     await message.answer(f'Next question:\nQuestion: {question_text}\nLevel: {level}')
    #
    #     # Update the user's state to 'answer'
    #     await state.update_data(
    #         question_id=next_question['question_id'],
    #         level_id=level,
    #         answer_text=next_question['answer_text']
    #     )
    # else:
    #     await message.answer('You have completed the quiz!')
    #     await state.clear()

    # Get the number of questions remaining to answer
    num_questions = user_data.get('num_questions', 0)
    num_questions -= 1

    if num_questions > 0:
        # Continue with the next question
        await state.update_data(num_questions=num_questions)
        next_question = get_next_question(question_id)
        if next_question:
            # Show the next question
            question_text = next_question['question_text']
            level = next_question['level_id']
            await message.answer(f'Next question:\nQuestion: {question_text}\nLevel: {level}')

            # Update the user's state to 'answer'
            await state.update_data(
                question_id=next_question['question_id'],
                level_id=level,
                answer_text=next_question['answer_text'],
                subject_name=next_question['subject_name']
            )
        else:
            await message.answer('You have completed the quiz!')
            await state.clear()
            await message.answer('Please select the subject you would like to test:', reply_markup=subjects)
            await state.set_state(Form.START_TEST)
    else:
        # User has answered all questions, go back to main menu
        await message.answer('You have answered all the questions!')
        await state.clear()
        await message.answer('Please select the subject you would like to test:', reply_markup=subjects)
        await state.set_state(Form.START_TEST)


def get_questions_for_subject(subject_name):
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        """SELECT
         q.question_id, q.subject_name, q.question_text, q.answer_text, q.level_id, q.explanation_text 
         FROM questions q 
         WHERE q.subject_name = %s
         ;""", (subject_name,)
    )
    questions = []
    rows = cur.fetchall()
    for row in rows:
        question = {
            'question_id': row[0],
            'subject_name': row[1],
            'question_text': row[2],
            'answer_text': row[3],
            'level_id': row[4],
            'explanation_text': row[5]
        }

        questions.append(question)
    cur.close()
    connection_pool.putconn(conn)
    return questions


def get_questions_for_subject_by_username(subject_name, username):
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT q.question_id, q.subject_name, q.question_text, q.answer_text, q.level_id, q.explanation_text
        FROM questions q
        JOIN levels l ON q.level_id = l.level_id
        WHERE q.subject_name = %s -- Replace with the desired subject
        AND q.question_id NOT IN (
            SELECT uq.question_id
            FROM user_questions uq
            JOIN users u ON uq.username = u.username
            WHERE u.username = %s -- Replace with the specific username
        );
         ;""", (subject_name, username)
    )
    questions = []
    rows = cur.fetchall()
    for row in rows:
        question = {
            'question_id': row[0],
            'subject_name': row[1],
            'question_text': row[2],
            'answer_text': row[3],
            'level_id': row[4],
            'explanation_text': row[5]
        }

        questions.append(question)
    cur.close()
    connection_pool.putconn(conn)
    return questions


def get_first_question():
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        """SELECT q.question_id, q.subject_name, q.question_text, q.answer_text, q.level_id, q.explanation_text 
         FROM questions q ORDER BY q.question_id LIMIT 1;"""
    )

    row = cur.fetchone()
    question = {
        'question_id': row[0],
        'subject_name': row[1],
        'question_text': row[2],
        'answer_text': row[3],
        'level_id': row[4],
        'explanation_text': row[5]
    }
    cur.close()
    connection_pool.putconn(conn)
    return question


def store_user_answer(question_id, username, level_id, subject_name):
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_questions (question_id, username, level_id, subject_name) VALUES (%s, %s, %s, %s);",
        (question_id, username, level_id, subject_name)
    )
    conn.commit()
    cur.close()
    connection_pool.putconn(conn)


def get_next_question(question_id):
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        """SELECT q.question_id, q.subject_name, q.question_text, q.answer_text, q.level_id, q.explanation_text 
         FROM questions q WHERE q.question_id > %s ORDER BY question_id LIMIT 1;""",
        (question_id,)
    )

    row = cur.fetchone()
    next_question = {
        'question_id': row[0],
        'subject_name': row[1],
        'question_text': row[2],
        'answer_text': row[3],
        'level_id': row[4],
        'explanation_text': row[5]
    }
    cur.close()
    connection_pool.putconn(conn)
    return next_question


# Define a function to get statistics
def get_statistics(username):
    conn = connection_pool.getconn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT uq.subject_name, COUNT(*) as correct_answers
        FROM user_questions uq
        JOIN questions q ON uq.question_id = q.question_id
        WHERE uq.username = %s AND uq.subject_name = q.subject_name
        GROUP BY uq.subject_name;
        """, (username,)
    )
    subjects = []
    statistics = cur.fetchall()

    for subject in statistics:
        subjects.append({'subject_name': subject[0],
                         'correct_answers': subject[1]})
    cur.close()
    connection_pool.putconn(conn)
    return subjects
