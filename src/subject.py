class Subject:
    """
    @author Roy Meoded
    @author Noa Agassi
    The Subject interface declares methods for attaching, detaching, and notifying observers.
    """
    def __init__(self):
        self._observers = []  # List to store observers

    def attach(self, observer):
        """
        Attach an observer to the subject.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Detach an observer from the subject.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update(self)