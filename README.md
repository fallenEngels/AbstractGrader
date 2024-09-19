# Scientific Abstract Grader
Have you ever done a literature review and needed to pre-select papers that fit or do not fit your research question? Or tried to group papers together based on overarching themes or approaches?
Have you done any of these steps in a Word or Excel document (or any equivalents) that wasn't designed for this purpose and turned everything into a headache?

Me too, but I wrote some code to make my life easier.

# How it works
All you need is a CSV file where each row is one paper you want to evaluate. As a minimum, this program expects two columns to be present: One containing the work's title, and one containing the work's abstract.
You can of course feel free to replace these with whatever information you deem relevant, but keep in mind that the fields tied to each column were designed to fit titles and abstracts respectively, so issues may occur.

The program then either adds a new column, or uses a pre-existing column (in case you want to continue where you left off), to store your evaluations right besides all existing information.

# Options
The options window allows you to specify a research question. Whatever you put in here will be displayed right above the evaluation buttons in the main window, so that you can refer back to your obective at any time. This is meant to increase evaluation consistency.
Additionally, the options window lets you specify the labels for up to 5 evaluation options to be displayed in the app. Two important things are to note:
1. Whatever labels you use here will be written into the CSV file as the paper's evaluation. Pick labels you will understand while evaluating AND when referring back to them at a later date.
2. You can clear the labels from a button to hide it in the main window, meaning you can either use all 5 categories or simplify the evaluation down to "yes"/"no" without further distractions.

# Requirements
This is Python code and as such requires Python.
Packages required are: `pandas` to save, load and edit CSV files and `PySide6` for the UI.
