import json, jsonpointer, pandas

class NestedDataParser:
    """
    Performs an aggregation on a nested structure of dicts, tuples, and lists,
    given a configuration of JSON pointers and mapping functions
    """
    def pointer(data, config, callback):
        """
        Resolves the jsonpointer in config['pointer'] on data argument, and
        calls callback with the result of that resolution,
        then returns the result.
        For example, NestedDataParser.pointer({'a': 'x'}, {'pointer':'/a'}, lambda item: item) returns 'x'
        """
        return callback(jsonpointer.resolve_pointer(data, config['pointer']))

    def join(data, config, callback):
        """
        Calls callback for each of the elements of data and converts each value return by callback to string
        Next it, joins the result by config['separator']
        For example, NestedDataParser.join(['a','b'], {'separator':', '}, lambda item: item) returns 'a, b'
        """
        result = list(map(lambda item: str(callback(item)), data))
        return config['separator'].join(result)

    # Turns a None into a 0
    def recode(data, config, callback):
        """
        Calls callback with data, then recodes the result by replacing data by 
        config['replacements'][data], if that key exists, else keeps data as is
        return that recoded result
        For example, NestedDataParser.recode('a', {'replacements':{'a': 'b', None: 'c'}}, lambda item: item) returns 'b'
        """
        result = callback(data)
        if data in config['replacements'].keys():
            result = config['replacements'][result]
        return result

    # Counts number of elements not None
    def count(data, config, callback):
        """
        Takes data, calls callback for each of its elements, returns the number of results that is not None
        For example: ["a", "b", "c"] gets converted to 3
        """
        result = list(map(lambda item: callback(item), data))
        result = [item for item in result if item is not None]
        return len(result)
    
    # names for each mapping function as used in the aggregation config
    mappings = {
        'pointer': pointer,
        'join': join,
        'recode': recode,
        'count': count
    }

    def resolve(data, config):
        """
        Recursively 
        """
        try:    
            # No more config left? Return the data
            if len(config) == 0:
                return data
            # Config left; create a callback to be called by the current mapping function
            def callback(data):
                return NestedDataParser.resolve(
                    data,
                    config[1:]
                )
            # Get current mapping function from config
            mapping_function = NestedDataParser.mappings[config[0]['type']]
            # Call the mapping function on data, passing on the callback and config
            return mapping_function(data, config[0], callback)
        except Exception as e:
            # Catch exception and return config['except'] if config['except'] exists
            if 'except' in config[0]:
                return config[0]['except']
            # Raise another exception with config info 
            raise Exception('An exception occurred with config ' + str(config[0]))
            #raise e


