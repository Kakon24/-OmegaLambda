import json
import logging

_config = None

def get_config():
    '''

    Raises
    ------
    NameError
        Meant only as a way to retrieve an already initialized global config object, so if that object has not
        been created yet, we raise a name error.

    Returns
    -------
    _config : CLASS INSTANCE OBJECT of Config
        Based off of a dictionary generated from a .json config file.  Global object to be passed anywhere
        it is needed.

    '''
    global _config
    if _config is None:
        logging.error('Global config object was called before being initialized')
        raise NameError('Global config object has not been initialized')
    else:
        logging.debug('Global config object was called')
        return _config

class Config():
    
    def __init__(self, cooler_setpoint=None, cooler_idle_setpoint=None, cooler_settle_time=None, maximum_jog=None, site_latitude=None, 
                 site_longitude=None, humidity_limit=None, wind_limit=None, weather_freq=None, focus_exposure_multiplier=None, initial_focus_delta=None,
                 focus_iterations=None, focus_goal=None, data_directory=None, home_directory=None, prep_time=None):
        '''

        Parameters
        ----------
        cooler_setpoint : INT, optional
            Setpoint in C when running camera cooler.  Our default is -30 C.
        cooler_idle_setpoint : INT, optional
            Setpoint in C when not running camera cooler.  Our default is +5 C.
        cooler_settle_time : INT, optional
            Time in minutes given for the cooler to settle to its setpoint. Our default is 5-10 minutes.
        maximum_jog : INT, optional
            Maximum distance in arcseconds to be used for the telescope jog function. Our default is 1800 arcseconds.
        site_latitude : FLOAT, optional
            Latitude at the telescope location.  Our default is +38.828 degrees.
        site_longitude : FLOAT, optional
            Longitude at the telescope location.  Our default is -77.305 degrees.
        humidity_limit : INT, optional
            Limit for humidity while observing.  Our default is 85%.
        wind_limit : INT, optional
            Limit for wind speed in mph while observing.  Our default is 20 mph.
        weather_freq : INT, optional
            Frequency of weather checks in minutes.  Our default is 15 minutes.
        focus_exposure_multiplier : FLOAT, optional
            Multiplier for exposure times on focusing images.  The multiplier is applied to the exposure time for the current ticket.  Our default is 0.5.
        initial_focus_delta : INT, optional
            Initial number of steps the focuser will move for each adjustment.  Our default is 10 steps.
        focus_iterations : INT, optional
            Maximum number of times to adjust the focuser before settling for the current focus.  Our default is 10.
        focus_goal : INT or FLOAT, optional
            FWHM in arcseconds that the focuser should strive to achieve within the maximum number of iterations.  Our default is 10 arcseconds.
        data_directory : STR, optional
            Where images and other data are saved on the computer.  Our default is H:/Observatory Files/Observing Sessions/2020_Data.
        home_directory : STR, optional
            Where the home of our code base is.  Our default is C:/Users/GMU Observtory1/-omegalambda.
        prep_time : INT, optional
            Preparation time in minutes needed before an observation run to take darks and flats.  Our default is 30 minutes.

        Returns
        -------
        None.

        '''
        self.cooler_setpoint = cooler_setpoint                      
        self.cooler_idle_setpoint = cooler_idle_setpoint            
        self.cooler_settle_time = cooler_settle_time                
        self.maximum_jog = maximum_jog                             
        self.site_latitude = site_latitude                    
        self.site_longitude = site_longitude                
        self.humidity_limit = humidity_limit                      
        self.wind_limit = wind_limit                         
        self.weather_freq = weather_freq      
        self.focus_exposure_multiplier = focus_exposure_multiplier
        self.initial_focus_delta = initial_focus_delta
        self.focus_iterations = focus_iterations
        self.focus_goal = focus_goal                  
        self.data_directory = data_directory                     
        self.home_directory = home_directory                        
        self.prep_time = prep_time
        
    @staticmethod
    def deserialized(text):
        '''

        Parameters
        ----------
        text : STR
            Pass in a json-formatted STR received from our json_reader and object_readers that is to be decoded into
            a python dictionary. Then, using the object_hook, that dictionary is transformed into our Config class
            object.

        Returns
        -------
        CLASS INSTANCE OBJECT of Config
            Global config class object to be used by any other process that needs it.  Once it has been created,
            it can be called repeatedly thereafter using get_config.

        '''
        return json.loads(text, object_hook=_dict_to_config_object)
    
    def serialized(self):
        '''

        Returns
        -------
        DICT
            A way to use the config class object as a traditional dictionary, rather than the self-properties
            defined in __init__.

        '''
        return self.__dict__
    
def _dict_to_config_object(dict):
    '''

    Parameters
    ----------
    dict : DICT
        A dictionary of our config file, generated using json.loads from deserialized.

    Returns
    -------
    _config : CLASS INSTANCE OBJECT of Config
        Global config class object that is also returned by deserialized.

    '''
    global _config
    _config = Config(cooler_setpoint=dict['cooler_setpoint'], cooler_idle_setpoint=dict['cooler_idle_setpoint'],
                     cooler_settle_time=dict['cooler_settle_time'], site_latitude=dict['site_latitude'], site_longitude=dict['site_longitude'], 
                     maximum_jog=dict['maximum_jog'], humidity_limit=dict['humidity_limit'], wind_limit=dict['wind_limit'], weather_freq=dict['weather_freq'],
                     focus_exposure_multiplier=dict['focus_exposure_multiplier'], initial_focus_delta=dict['initial_focus_delta'],
                     focus_iterations=dict['focus_iterations'], focus_goal=dict['focus_goal'], data_directory=dict['data_directory'], 
                     home_directory=dict['home_directory'], prep_time=dict['prep_time'])
    logging.info('Global config object has been created')
    return _config