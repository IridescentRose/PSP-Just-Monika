init -999:
    default persistent._mas_submod_version_data = dict()
init offset = -990
init 1000 python:

    store.mas_submod_utils.Submod._checkUpdates()

init 1 python:

    store.mas_submod_utils.Submod._checkDependencies()

init python in mas_ui:
    import store
    has_submod_settings = len([
        submod
        for submod in store.mas_submod_utils.submod_map.values()
        if submod.settings_pane is not None
    ]) > 0

init -1 python in mas_submod_utils:
    import store
    import sys
    import traceback

    persistent = store.persistent

    submod_map = dict()

    class SubmodError(Exception):
        def __init__(self, _msg):
            self.msg = _msg
        def __str__(self):
            return self.msg

    class Submod:
        """
        Submod class

        PROPERTIES:
            author - submod author
            name - submod name
            description - submod description
            version - version of the submod installed
            dependencies - dependencies required for the submod
            settings_pane - string referring to the screen used for the submod's settings
            version_updates - update labels
        """
        
        FB_VERS_STR = "0.0.0"
        
        def __init__(
            self,
            author,
            name,
            description,
            version,
            dependencies={},
            settings_pane=None,
            version_updates={}
        ):
            """
            Submod object constructor

            IN:
                author - string, author name.

                name - submod name

                description - a short description for the submod

                version - version number in format SPECIFICALLY like so: `1.2.3`
                    (You can add more or less as need be, but splits MUST be made using periods)

                dependencies - dictionary in the following structure: {"name": ("minimum_version", "maximum_version")}
                corresponding to the needed submod name and version required
                NOTE: versions must be passed in the same way as the version property is done
                    (Default: empty dict)

                settings_pane - a string representing the screen for this submod's settings

                version_updates - dict of the format {"old_version_update_label_name": "new_version_update_label_name"}
                    NOTE: submods MUST use the format <author>_<name>_v<version> for update labels relating to their submods
                    NOTE: capital letters will be forced to lower and spaces will be replaced with underscores
                    NOTE: Update labels MUST accept a version parameter, defaulted to the version of the label
                    For example:
                        author name: MonikaAfterStory,
                        submod name: Example Submod
                        submod vers: 1.2.3

                    becomes:
                        label monikaafterstory_example_submod_v1_2_3(version="v1_2_3")
            """
            
            if name in submod_map:
                store.mas_utils.writelog("[SUBMOD ERROR]: A submod with name '{0}' already exists. Ignoring.\n".format(name))
                return
            
            
            try:
                map(int, version.split('.'))
            except:
                raise SubmodError("Version number '{0}' is invalid.".format(version))
            
            
            self.author = author
            self.name = name
            self.description = description if description is not None else ""
            self.version = version
            self.dependencies = dependencies
            self.settings_pane = settings_pane
            self.version_updates = version_updates
            
            
            submod_map[name] = self
            
            
            if name not in persistent._mas_submod_version_data:
                persistent._mas_submod_version_data[name] = version
        
        def getVersionNumberList(self):
            """
            Gets the version number as a list of integers

            OUT:
                List of integers representing the version number
            """
            return map(int, self.version.split('.'))
        
        def hasUpdated(self):
            """
            Checks if this submod instance was updated (version number has incremented)

            OUT:
                boolean:
                    - True if the version number has incremented from the persistent one
                    - False otherwise
            """
            old_vers = persistent._mas_submod_version_data.get(self.name)
            
            
            if not old_vers:
                return False
            
            try:
                old_vers = map(int, old_vers.split('.'))
            
            
            except:
                persistent._mas_submod_version_data[self.name] = Submod.FB_VERS_STR
                return False
            
            return self.checkVersions(old_vers) > 0
        
        def updateFrom(self, version):
            """
            Updates the submod, starting at the given start version

            IN:
                version - the version number in the parsed format ('author_name_v#_#_#')
            """
            while version in self.version_updates:
                updateTo = self.version_updates[version]
                
                
                if renpy.has_label(updateTo) and not renpy.seen_label(updateTo):
                    renpy.call_in_new_context(updateTo, updateTo)
                version = self.version_updates[version]
        
        def checkVersions(self, comparative_vers):
            """
            Generic version checker for submods

            IN:
                curr_vers - current installed version of the submod as a list
                comparative_vers - the version we're comparing to (or need the current version to be at or greater than) as a list

            OUT:
                integer:
                    - (-1) if the current version number is less than the comparitive version
                    - 0 if the current version is the same as the comparitive version
                    - 1 if the current version is greater than the comparitive version
            """
            return store.mas_utils.compareVersionLists(
                self.getVersionNumberList(),
                comparative_vers
            )
        
        @staticmethod
        def _checkUpdates():
            """
            Checks if submods have updated and sets the appropriate update scripts for them to run
            """
            
            for submod in submod_map.itervalues():
                
                if submod.hasUpdated():
                    submod.updateFrom(
                        "{0}_{1}_v{2}".format(
                            submod.author,
                            submod.name,
                            persistent._mas_submod_version_data.get(submod.name, Submod.FB_VERS_STR).replace('.', '_')
                        ).lower().replace(' ', '_')
                    )
                
                
                persistent._mas_submod_version_data[submod.name] = submod.version
        
        @staticmethod
        def _checkDependencies():
            """
            Checks to see if the dependencies for this submod are met
            """
            def parseVersions(version):
                """
                Parses a string version number to list format.

                IN:
                    version - version string to parse

                OUT:
                    list() - representing the parsed version number

                NOTE: Does not handle errors as to get here, formats must be correct regardless
                """
                return map(int, version.split('.'))
            
            for submod in submod_map.itervalues():
                for dependency, minmax_version_tuple in submod.dependencies.iteritems():
                    dependency_submod = Submod._getSubmod(dependency)
                    
                    if dependency_submod is not None:
                        
                        minimum_version, maximum_version = minmax_version_tuple
                        
                        
                        if (
                            minimum_version
                            and dependency_submod.checkVersions(parseVersions(minimum_version)) < 0
                        ):
                            raise SubmodError(
                                "Submod '{0}' is out of date. Version {1} required for {2}. Installed version is {3}".format(
                                    dependency_submod.name, minimum_version, submod.name, dependency_submod.version
                                )
                            )
                        
                        
                        
                        elif (
                            maximum_version
                            and dependency_submod.checkVersions(parseVersions(maximum_version)) > 0
                        ):
                            raise SubmodError(
                                "Version '{0}' of '{1}' is installed and is incompatible with {2}.\nVersion {3} is compatible.".format(
                                    dependency_submod.version, dependency_submod.name, submod.name, maximum_version
                                )
                            )
                    
                    
                    else:
                        raise SubmodError(
                            "Submod '{0}' is not installed and is required for {1}.".format(
                                dependency, submod.name
                            )
                        )
        
        @staticmethod
        def _getSubmod(name):
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object representing the submod by name if installed and registered
                None if not found
            """
            return submod_map.get(name)


    def isSubmodInstalled(name, version=None):
        """
        Checks if a submod with `name` is installed

        IN:
            name - name of the submod to check for
            version - if a specific version (or greater) is installed
            (NOTE: if None, this is ignored. Default: None)

        OUT:
            boolean:
                - True if submod with name is installed
                - False otherwise
        """
        submod = Submod._getSubmod(name)
        
        if submod and version:
            return submod.checkVersions(version) >= 0
        return bool(submod)


init 10 python in mas_submod_utils:
    import inspect
    import store


    current_label = None

    last_label = None


    function_plugins = dict()


    DEF_PRIORITY = 0


    JUMP_CALL_PRIORITY = 999

    PRIORITY_SORT_KEY = lambda x: x[1][2]


    def functionplugin(_label, _args=[], auto_error_handling=True, priority=0):
        """
        Decorator function to register a plugin

        The same as registerFunction. See its doc for parameter details
        """
        def wrap(_function):
            registerFunction(
                _label,
                _function,
                _args,
                auto_error_handling,
                priority
            )
            return _function
        return wrap


    def getAndRunFunctions(key=None):
        """
        Gets and runs functions within the key provided

        IN:
            key - Key to retrieve and run functions from
        """
        global function_plugins
        
        
        if not key:
            key = inspect.stack()[1][3]
        
        func_dict = function_plugins.get(key)
        
        if not func_dict:
            return
        
        
        sorted_plugins = _m1_zz_submods__prioritySort(key)
        for _action, data_tuple in sorted_plugins:
            if data_tuple[1]:
                try:
                    store._m1_zz_submods__run(_action, getArgs(key, _action))
                except Exception as ex:
                    store.mas_utils.writelog("[ERROR]: function {0} failed because {1}\n".format(_action.__name__, ex))
            
            else:
                store._m1_zz_submods__run(_action, getArgs(key, _action))

    def registerFunction(key, _function, args=[], auto_error_handling=True, priority=DEF_PRIORITY):
        """
        Registers a function to the function_plugins dict

        NOTE: Does NOT allow overwriting of existing functions in the dict
        NOTE: Function must be callable
        NOTE: Functions run when a label matching the key for the function is:
        called, jumped, or fallen through to.
        Or if plugged into a function, when a function by the name of the key calls getAndRunFunctions

        IN:
            key - key to add the function to.
                NOTE: The key is either a label, or a function name
                NOTE: Function names only work if the function contains a getAndRunFunctions call.
                    Without it, it does nothing.
            _function - function to register
            args - list of args (must be in order) to pass to the function
                (Default: [])
            auto_error_handling - whether or function plugins should ignore errors in functions
                (Set this to False for functions which call or jump)
            priority - Order priority to run functions
                (Like init levels, the lower the number, the earlier it runs)

        OUT:
            boolean:
                - True if the function was registered successfully
                - False otherwise
        """
        global function_plugins
        
        
        if not callable(_function):
            store.mas_utils.writelog("[ERROR]: {0} is not callable\n".format(_function.__name__))
            return False
        
        
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.writelog("[ERROR]: Too many args provided for function {0}\n".format(_function.__name__))
            return False
        
        
        key = _m1_zz_submods__getOverrideLabel(key)
        
        
        if key not in function_plugins:
            function_plugins[key] = dict()
        
        
        elif _function in function_plugins[key]:
            return False
        
        function_plugins[key][_function] = (args, auto_error_handling, priority)
        return True

    def getArgs(key, _function):
        """
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        global function_plugins
        
        func_dict = function_plugins.get(key)
        
        if not func_dict:
            return
        
        return func_dict.get(_function)[0]

    def setArgs(key, _function, args=[]):
        """
        Sets args for the given function at the key

        IN:
            key - key that the function's function dict is stored in
            _function - function to set the args
            args - list of args (must be in order) to pass to the function (Default: [])

        OUT:
            boolean:
                - True if args were set successfully
                - False if not
        """
        global function_plugins
        
        func_dict = function_plugins.get(key)
        
        
        if not func_dict:
            return False
        
        
        elif _function not in func_dict:
            return False
        
        
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.writelog("[ERROR]: Too many args provided for function {0}\n".format(_function.__name__))
            return False
        
        
        old_values = func_dict[_function]
        func_dict[_function] = (args, old_values[1], old_values[2])
        return True

    def unregisterFunction(key, _function):
        """
        Unregisters a function from the function_plugins dict

        IN:
            key - key the function we want to unregister is in
            _function - function we want to unregister

        OUT:
            boolean:
                - True if function was unregistered successfully
                - False otherwise
        """
        global function_plugins
        
        func_dict = function_plugins.get(key)
        
        
        if not func_dict:
            return False
        
        
        elif _function not in func_dict:
            return False
        
        
        function_plugins[key].pop(_function)
        return True

    def _m1_zz_submods__prioritySort(_label):
        """
        Sorts function plugins based on the priority order system

        IN:
            _label - label to sort functions by priority for

        OUT:
            sorted list of (_function, data_tuple) tuples

        NOTE: This assumes that the label exists in the function_plugins dict
        """
        global function_plugins
        
        
        func_list = [
            (_function, data_tuple)
            for _function, data_tuple in function_plugins[_label].iteritems()
        ]
        
        return sorted(func_list, key=PRIORITY_SORT_KEY)

    def _m1_zz_submods__getOverrideLabel(_label):
        """
        Gets the override label for the given label (will follow the chain if overrides are overridden)

        IN:
            _label - label to get the override label for

        OUT:
            string representing the last label in the override chain or _label if there are no overrides
        """
        while renpy.config.label_overrides.get(_label) is not None:
            _label = renpy.config.label_overrides[_label]
        return _label


init python:
    def _m1_zz_submods__run(_function, args):
        """
        Private function to run a function in the global store
        """
        return _function(*args)


init 1989 python:
    def label_callback(name, abnormal):
        """
        Function to run plugin functions and store the last label
        """
        
        store.mas_submod_utils.last_label = store.mas_submod_utils.current_label
        
        store.mas_submod_utils.current_label = name
        
        store.mas_submod_utils.getAndRunFunctions(name)

    config.label_callback = label_callback
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
