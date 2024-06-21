class LPS:
    def __init__(self, device_connection, *args):
        pass

    @property
    def commands(self):
        """Return commands dictionary

        Returns
        -------
        commands : dict
            commands that the device supports
        """
        return {"move_plugin_device": lambda *args: self.move(args[0])}

    def get_class_names(self):
        """Return the class names in the library.

        See the corresponding 32-bit :meth:`~.dotnet32.DotNet32.get_class_names` method.

        Returns
        -------
        :class:`list` of :class:`str`
            The names of the classes that are available in :ref:`dotnet_lib32.dll <dotnet-lib>`.        
        """
       