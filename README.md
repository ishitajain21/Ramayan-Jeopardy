# Ramayan Jeopardy

## Overview
Ramayan Jeopardy is an interactive quiz game inspired by the classic game show **Jeopardy!**, featuring questions based on the Indian epic, the *Ramayana*. Players can test their knowledge across different categories and difficulty levels, making it an engaging way to learn about this ancient scripture.

## Features
- **Multiple Categories**: Questions are divided into different themes such as Characters, Events, Places, and Morals.
- **Bonus Round**: A special round with additional questions for extra points.
- **Multiple Players**: Supports multiple teams competing against each other.
- **Point Scoring System**: Earn points for correct answers, with higher points for more challenging questions.

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ramayan-jeopardy.git
   ```
2. Navigate into the project directory:
   ```sh
   cd ramayan-jeopardy
   ``` 
   ```
3. Run the application:
   Double click on the file to open in file explorer. 

## How to Change Questions
To modify the questions, follow these steps:
1. Open the `jeo.html` file in a text editor.
2. Locate the `gameData` object inside the `<script>` section.
3. Find the `questions` dictionary within `gameData`. The structure follows:
   ```js
   'Category Name': {
       PointValue: { q: 'Question text', a: 'Answer text' },
   }
   ```
   Example:
   ```js
   'Epic Origins': {
       200: { q: 'This sage is credited with writing the original Ramayan', a: 'Valmiki' },
   }
   ```
4. Edit the existing questions or add new ones following the same format.
5. Save the file and restart the game to apply changes.

## How to Play
1. Choose a category and difficulty level.
2. Answer the question presented on the screen.
3. Earn points based on the correctness of your answer.
4. Continue playing until all questions are answered.
5. The player with the highest score wins!

## Contribution
Contributions are welcome! To contribute:
- Fork the repository
- Create a new branch (`feature/your-feature`)
- Commit your changes
- Open a pull request

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any inquiries or suggestions, feel free to reach out via email or open an issue in the repository.

Enjoy playing **Ramayan Jeopardy** and deepen your understanding of this legendary epic! 🎮📖

