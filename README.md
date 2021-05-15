# tkinterSuggestion
Active Dropdown Suggestions for Tkinter Entry

This project enables a Tkinter Entry Widget to display a dropdown list of values that can be updated as user keys in text to the widget.

The drop downm list can be updated with desired values.

Import the GetSuggestion file into your project.

Usage:

Create an object of the class GetSuggestion, Following parameters are expected.

1) Base window object on top of which the dropdown window will be created.
2) Entry Widget for which the dropdown suggestion is needed.
3) X position of the Dropdown window
4) Y position of the Dropdown window
5) Width of the Window
6) Height of the window
7) Callback function, which will be called to update the List of values. It is expected to have two Parameters. One for the Current Text in the Entry Widget, and a Flag that is set to 1 when a value is selected. The callback function is expected to update the list based on the current values and call setSuggestionList to update the list in screen.
8) The text variable of the Entry widget, which will have the selected value.

Example:
getSuggestionObject = GetSuggestion(<baseWindow>, <EntryWidget>, <windowX>, <windowY>, <Length>, <Height>, <callBack Function>, <Entry Text Variable>)

Review the sample code provided in liveSuggestion.py as an example to use it.

![image](https://user-images.githubusercontent.com/44316307/118353359-7bf61480-b583-11eb-83ec-5aada804b0c8.png)

![image](https://user-images.githubusercontent.com/44316307/118353404-a6e06880-b583-11eb-879d-36ebd03c3922.png)

![image](https://user-images.githubusercontent.com/44316307/118353513-34bc5380-b584-11eb-9906-c652ab6d9fd4.png)

![image](https://user-images.githubusercontent.com/44316307/118353453-e313c900-b583-11eb-84d2-02afd23f7ced.png)

