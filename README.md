Ramayan Jeopardy

Overview

Ramayan Jeopardy is an interactive quiz game inspired by the classic game show Jeopardy!, featuring questions based on the Indian epic, the Ramayana. Players can test their knowledge across different categories and difficulty levels, making it an engaging way to learn about this ancient scripture.

Features

Multiple Categories: Questions are divided into different themes such as Characters, Events, Places, and Morals.

Bonus Round: A special round with additional questions for extra points.

Multiple Players: Supports multiple teams competing against each other.

Point Scoring System: Earn points for correct answers, with higher points for more challenging questions.

How to Change Questions

To modify the questions, follow these steps:

Open the jeo.html file in a text editor.

Locate the gameData object inside the <script> section.

Find the questions dictionary within gameData. The structure follows:

'Category Name': {
    PointValue: { q: 'Question text', a: 'Answer text' },
}

Example:

'Epic Origins': {
    200: { q: 'This sage is credited with writing the original Ramayan', a: 'Valmiki' },
}

Edit the existing questions or add new ones following the same format.

Save the file and restart the game to apply changes.

How to Play

Choose a category and difficulty level.

Answer the question presented on the screen.

Earn points based on the correctness of your answer.

Continue playing until all questions are answered.

The player with the highest score wins!

Contribution

Contributions are welcome! To contribute:

Fork the repository

Create a new branch (feature/your-feature)

Commit your changes

Open a pull request
