class LoadingBar:
    """
    Py-Load main class.
    """
    def __init__(self, total: int, borderChars = ["[", "]"], progressChar: str = "#", emptyChar: str = " ", barLength = 50):
        """
        Initialize the Loading Bar.

        Customize the way it looks by specifying the `borderChars`, `progressChar`, and `emptyChar` arguements.

        You can do this by doing `<loadingBarName>.<arguementName> = <value>`. 
        This can also be specified when initializing.
        """

        self.total = total
        """The total/max value of the loading bar."""
        self.progress = 0
        """The progress value of the loading bar. Not a precentage."""
        self.borderChars = borderChars
        """
        Default: "[", "]"

        A list that should have two values, the opening border character and the closing border character.

        They surround the loading bar's progress meter.

        Eg:
        ```
        ...
        myLoadingBar.borderChars = ["{", "}"]
        myLoadingBar.display()
        ```
        Output: `{##########}`
        """
        self.progressChar = progressChar
        """
        Default: "#"

        The progress character / the fill character.
        """
        self.emptyChar = emptyChar
        """
        Default: " " (space)

        The empty character
        """
        self.barLength = barLength
        """
        Default: 50

        The length (in characters) of the loading bar.
        """
    
    def display(self):
        """
        Display the Loading Bar.
        """
        percent = round((self.progress / self.total) * self.barLength)

        toPrint = ""
        toPrint += self.borderChars[0]
        for i in range(percent):
            if len(toPrint) < (self.barLength + len(self.borderChars[0])):
                toPrint += self.progressChar
        for i in range(self.barLength - percent):
            toPrint += self.emptyChar
        
        toPrint += self.borderChars[1]

        return(toPrint)