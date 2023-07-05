import obspython as obs
import urllib.request
import urllib.error
import json
import datetime

# Global settings
url         = ""
interval    = 10
continuous_update = False
autohide_job_info = False
job_info_source_name = ""

# ----------------------------------------------------
# Description displayed in the Scripts dialog window
def script_description():
    return """Reads the telemetry data of Euro Truck Simulator 2 and modifies a Text source with it.
    To display data from the telemetry create a Text(GDI+) source and rename it with 'ETS2' as prefix and
    the information you want, separated by '-', for example: 'ETS2-game-connected'"""

# Called after change of settings including once after script load
def script_update(settings):
    global url, interval, continuous_update, autohide_job_info, job_info_source_name
    url = obs.obs_data_get_string(settings, "url")
    interval = obs.obs_data_get_int(settings, "interval")
    autohide_job_info = obs.obs_data_get_bool(settings, "autohide_job_info")
    job_info_source_name = obs.obs_data_get_string(settings, "job_info_source_name")

    obs.timer_remove(update_text)
    if url!= "":
        obs.timer_add(update_text, interval * 1000)

# Called to set default vaues of data settings
def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "url", "")
    obs.obs_data_set_default_int(settings, "interval", 10)
    obs.obs_data_set_default_bool(settings, "autohide_job_info", False)
    obs.obs_data_set_default_string(settings, "job_info_source_name", "")

# Called to display the properties GUI
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "url", "URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "interval", "Update interval (s)", 1, 30, 1)
    obs.obs_properties_add_bool(props, "autohide_job_info", "Auto-hide Job info")
    obs.obs_properties_add_text(props, "job_info_source_name", "Job info source", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props

# Called before data settings are saved
def script_save(settings):
    obs.obs_save_sources()

# ----------------------------------------------------
# Updates text propertie of Text(GDI+) source
def update_text():
    global url, interval, autohide_job_info, job_info_source_name
    if url != '':
        sources = obs.obs_enum_sources()        
        if sources:
            try:
                with urllib.request.urlopen(url) as response:
                    data = json.load(response)
                    if autohide_job_info:
                        scene_item = get_sceneitem_from_source_name_in_current_scene(job_info_source_name)                
                        if scene_item:
                            obs.obs_sceneitem_set_visible(scene_item, data['trailer']['attached'])
                    source_text = ''
                    # Updates every source that has ETS2 in its name
                    for source in sources:
                        if "ETS2" in obs.obs_source_get_name(source):
                            source_text = obs.obs_source_get_name(source).split("-")[1:]
                            data_value = data[source_text[0].strip()][source_text[1].strip()]
                            text = clean_data(data_value, source_text[1])
                            settings = obs.obs_data_create()
                            obs.obs_data_set_string(settings, "text", text)
                            obs.obs_source_update(source, settings)
                            obs.obs_data_release(settings)

            except urllib.error.URLError as err:
                response_data = str(err.reason)
                obs.script_log(obs.LOG_WARNING, "Error opening URL '" + url + "': " + response_data)
                obs.remove_current_callback()
                obs.source_list_release(sources)
        obs.source_list_release(sources)

# Refresh data when Refresh button is pressed
def refresh_pressed(props, prop):
    update_text()

# Handle data from telemetry
def clean_data(data, source_text):
    # Manage specific data from telemetry
    match source_text:
        case 'mass':
            data = str(int(data/1000)) + 'T'
        case 'remainingTime':
            data = calculate_remainingTime(data)

    # Transform float data to int          
    if (type(data) == float):
        data = int(data)
    
    return str(data)

# Transforms remainingTime data from ISO(8601) time into Hours
def calculate_remainingTime(data):
    remainingTime = datetime.datetime.fromisoformat(data)
    if remainingTime.day > 1:
        return str(24*(remainingTime.day-1) + remainingTime.hour) + 'H'
    elif remainingTime.hour > 0:
        return str(remainingTime.hour) + 'H'
    elif remainingTime.minute > 0:
        return str(remainingTime.minute) + "M"
    else:
        return ""
    
# Retrieves the scene item of the given source name in the current scene or None if not found
def get_sceneitem_from_source_name_in_current_scene(name):
    result_sceneitem = None
    current_scene_as_source = obs.obs_frontend_get_current_scene()
    if current_scene_as_source:
        current_scene = obs.obs_scene_from_source(current_scene_as_source)
        result_sceneitem = obs.obs_scene_find_source_recursive(current_scene, name)
        obs.obs_source_release(current_scene_as_source)
    return result_sceneitem