# Final-Project

***Big Idea and Project Goal***

The goal of this project was to design and build a functional software application that helps users track and understand their personal spending. I chose this idea because budgeting is an everyday problem that affects almost everyone, especially students, and I wanted to create a tool that makes it easier to manage expenses, analyze habits, and stay aware of financial patterns. The Personal Expense Tracker allows users to log their expenses through a clear and simple interface, categorize them, and then visualize spending through charts and summaries. For example, a user could record their Food, Transportation, and Shopping expenses throughout the month and then quickly see where most of their budget is going. My intention was to create an application that feels practical and intuitive, while also allowing me to apply the software design concepts taught in this course.

***User Instructions***



***Implementation Information***

This project was built primarily in Python, using Flask to create the web interface and manage routing between different pages of the application. Matplotlib is used to generate bar charts and pie charts that summarize spending patterns. JSON files serve as the data storage system for both expense entries and budgets, which keeps the project lightweight and easy to run without needing a separate database.

The application is organized into several components. The app.py file contains all backend logic such as loading and saving data, filtering expenses, generating charts, and evaluating spending against user-defined budgets. Each page of the website is built using HTML templates, which are stored in the templates folder and structured with Jinja to display data dynamically. I designed functions to separate major tasks such as calculating summaries, applying filters, producing charts, and managing budgets. This helped keep the project organized and easier to understand.

Although I did not include formal flowcharts in this README, the program follows a straightforward structure. When a user performs an action, such as adding an expense, the data is sent through a Flask route, processed by Python, saved to the JSON file, and then rendered back on the webpage. The chart generation process works similarly, but creates image files that are automatically displayed on the dashboard. This project gave me a chance to apply key principles of software design, including modularity, abstraction, and separation of concerns.

***Results***

The completed application includes a variety of features that work together to help users understand their finances. Users can add expenses with a date, category, amount, and optional note. They can view all expenses in a table that supports filtering by category, month, and year. The dashboard displays summaries such as total spending by category, average amount spent, and number of expenses.

To make the insights more visual, the app generates two charts: a bar chart of total spending by category and a pie chart showing the percentage share of each category. These charts automatically update based on the user’s filters, which gives a personalized view of spending patterns.

One of the strongest parts of the project is the budgeting feature. Users can set monthly budgets for different categories, and the dashboard compares the budget to actual spending. The app shows whether a category is within budget, nearing the limit, or over budget. This makes the tool feel more like a real personal finance application. The interface is styled with a green finance theme that creates a clean and cohesive look, and the ET logo adds a simple visual identity to the site.


***Project Evolution and Narrative***

This project grew significantly from the original idea. The initial plan was to create a simple command-line program that stored expenses and calculated basic summaries. Once I learned more about Flask and web development, I decided to expand the scope and turn it into a fully interactive web application. The project evolved step by step. I began with basic data storage functions, then built the add expense form, then added analytics, and finally implemented budgets and visual design.

Many improvements came from realizing what would make the tool easier to use. For example, adding dropdown menus prevented user errors, adding filters made the summaries more meaningful, and adding charts created a much more useful representation of spending. The budgeting feature was not part of the original plan but became one of the most valuable additions because it connects the app to real financial decision-making.

Throughout the process, I focused on creating a tool that felt practical and polished. The project taught me how software evolves through iteration and how features often connect in unexpected ways once the core foundations are in place.



