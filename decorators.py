from widgets.widgets import QuestionDialog
import functools

def exc_try(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            args[0].emit('updated','Done', 1)
        except Exception as e:
            args[0].emit('updated',str(e), 0)

    return wrapper

def check_dialog(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper(widget, *args, **kwargs):
        dialog = QuestionDialog(widget, "")
        response = dialog.run()

        if response == -8:#Gtk.ResponseType.YES
            func(widget, *args, **kwargs)
        elif response == -9:pass #Gtk.ResponseType.NO
        dialog.destroy()
    return wrapper
