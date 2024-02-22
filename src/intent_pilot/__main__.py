

if __name__ == "__main__":        
    from intent_pilot.run.app import main
    from intent_pilot.utils.system_utils import show_notification
    try:
        main()
    except Exception as err:
        print("Error")
        show_notification("intent-pilot",f"Error - {str(err)}")
        raise err