from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt
import os

# Had to use the os import as it just wasn't working at all without it at all :(
our_csv_path = os.path.join(os.path.dirname(__file__), 'cleaned_attendance_anonymised-1.csv')
# Quick note, do not run the above without running Exercise 2 and the beginning of 3 in the ipynb file
# As it creates the above csv

# Now we can actually load the data
the_summative_df = pd.read_csv(our_csv_path)

# Now, let's do the UI, with options for selecting the module and the title
ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "module_select",
            "Select Your Module",
            choices = the_summative_df['Module Name'].unique().tolist()
        ),
        title = "An Analysis of Attendance Data Across a Variety of Modules"
    ),
    ui.panel_title("Visualisation of Module Attendance"),
    ui.output_plot("john_attendance_plot")
)

# Onto the server
def server(input, output, session):
    @output
    @render.plot
    def john_attendance_plot():
        # Now, we place in code to filter the various modules
        his_lord_the_dataframe_of_modules = the_summative_df[the_summative_df['Module Name'] == input.module_select()]

        # Then we need to group by date and calculate the mean, as we did in Exercise 2
        modules_and_a_ten_dance = his_lord_the_dataframe_of_modules.groupby('Date')['Has Attended'].mean().reset_index()

        # We only do data science for the plot, found below!
        plt.figure(figsize=(16,6))
        plt.plot(modules_and_a_ten_dance['Date'], modules_and_a_ten_dance['Has Attended'])
        plt.title(f'Attendance Rate of {input.module_select()} Students Over Time')
        plt.xlabel('Date')
        plt.ylabel('Average Student Attendance')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
# Now, we display it in Streamlit
app = App(ui, server)