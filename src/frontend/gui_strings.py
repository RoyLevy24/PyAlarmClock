screen_helper = """
ScreenManager:
    MainScreen:
    AlarmFormScreen:
    # AlarmActiveScreen:
    # DismissSpeechScreen:



<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation:'vertical'
        MDToolbar:
            title: "Alarms"
            pos_hint: {"top": 1}
            elevation: 11
            right_action_items: [["plus", lambda x: root.create_alarm()]]


        ScrollView:
            id: scroll
            MDList:
                id: list

<AlarmFormScreen>:
    name: 'alarm_form'

    time_picker: time_picker
    check_days: [check_mon, check_tue, check_wen, check_thu, check_fri, check_sat, check_sun]
    tf_alarm_param: tf_alarm_param
    check_type: [check_speech, check_face, check_none]
    alarm_desc: alarm_desc

    MDToolbar:
        title: "Alarm Form"
        pos_hint: {"top": 1}
        elevation: 11

    MDBoxLayout:
        id: "alarm_form_main_box"
        orientation:'vertical'
        spacing: 5
        size_hint_y: .7
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        MDRectangleFlatIconButton:
            id: time_picker
            icon: "clock"
            text: "12:00"
            font_size: '70sp'
            height: dp(60)
            width: dp(250)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_press: root.open_time_picker()

        MDTextField:
            id: alarm_desc
            size_hint_x: .8
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            hint_text: "Enter Description"
            multiline: True


        MDBoxLayout:
            orientation:'horizontal'
            id: alarm_form_days_box
            padding: [20,20,20,20]
            size_hint_y: .2

            MDBoxLayout:
                id: alarm_from_day_mon
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Mon"

                MDCheckbox:
                    id: check_mon

            MDBoxLayout:
                id: alarm_form_day_tue
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Tue"

                MDCheckbox:
                    id: check_tue

            MDBoxLayout:
                id: alarm_form_day_tue
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Wen"

                MDCheckbox:
                    id: check_wen

            MDBoxLayout:
                id: alarm_form_day_thu
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Thu"

                MDCheckbox:
                    id: check_thu

            MDBoxLayout:
                id: alarm_form_day_fri
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Fri"
                
                MDCheckbox:
                    id: check_fri

            MDBoxLayout:
                id: alarm_form_day_sat
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Sat"

                MDCheckbox:
                    id: check_sat

            MDBoxLayout:
                id: alarm_form_day_sun
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Sun"

                MDCheckbox:
                    id: check_sun

        MDBoxLayout:
            orientation:'vertical'
            id: alarm_form_types_box
            size_hint_y: .2

            MDBoxLayout:
                orientation:'horizontal'
                id: alarm_from_types_checkboxes

                MDBoxLayout:
                    orientation:'vertical'
                    id: type_speech_box

                    MDLabel:
                        halign: "center"
                        valign: "center"
                        text: "Speech"

                    MDCheckbox:
                        name: "check_speech"
                        group: 'types'
                        id: check_speech
                        on_release: root.select_speech_alarm()

                MDBoxLayout:
                    orientation:'vertical'
                    id: type_face_box

                    MDLabel:
                        halign: "center"
                        valign: "center"
                        text: "Face"

                    MDCheckbox:
                        name: "check_face"
                        group: 'types'
                        id: check_face
                        on_release: root.select_face_alarm()

                MDBoxLayout:
                    orientation:'vertical'
                    id: type_none_box

                    MDLabel:
                        halign: "center"
                        valign: "center"
                        text: "None"

                    MDCheckbox:
                        name: "check_none"
                        id: check_none
                        active: True
                        group: 'types'
                        on_release: root.select_none_alarm()
                        

                
        MDTextField:
            id: tf_alarm_param
            size_hint_x: .5
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            hint_text: ""
            disabled: True

    MDToolbar:
        pos_hint: {"bottom": 1}
        elevation: 11
        right_action_items: [["check", lambda x: root.add_alarm()]]
        left_action_items: [["close", lambda x: root.back_to_alarm_list()]]


<AlarmActiveScreen>
    name: 'alarm_active'
    MDToolbar:
        title: "Alarm"
        pos_hint: {"top": 1}
        elevation: 11

    MDBoxLayout:
        id: "alarm_active_box"
        orientation: 'vertical'
        size_hint_y: .5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: [20,20,20,20]

        MDLabel:
            text: "12:00"
            halign: "center"
            valign: "center"
            markup: True
            font_style: "H1"

        MDLabel:
            text: "Test on Friday!"
            halign: "center"
            valign: "center"
            markup: True
            multiline: True
            font_style: "H6"

        Label:

        MDFillRoundFlatIconButton:
            icon: "cancel"
            text: "dismiss"
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            font_size: '30sp'

<DismissSpeechScreen>
    name: 'dismiss_speech'
    MDToolbar:
        title: "Dismiss Speech - 1/5"
        pos_hint: {"top": 1}
        elevation: 11
        
    MDBoxLayout:
        orientation: 'vertical'
        padding: [20,20,20,20]
        spacing: 5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: .7
        
        MDLabel:
            text: "Word"
            halign: "center"
            valign: "center"
            markup: True
            font_style: "H4"
            

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: "[wo-rd]"
                halign: "center"
                valign: "center"
                markup: True
                font_style: "H6"
            
            MDIconButton:
                icon: "play-circle"
                size_hint_y: .3
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        MDLabel:
            text: "This is the word's Description"
            halign: "center"
            valign: "center"
            markup: True
            font_style: "H6"
            multiline: True

        MDFloatingActionButton:
            icon: "microphone"
            elevation_normal: 10
            md_bg_color: app.theme_cls.primary_light
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    MDToolbar:
        title: "Next Word"
        pos_hint: {"bottom": 1}
        right_action_items: [["arrow-right-bold", lambda x: print("next word")]]

"""


alarm_string = """
ThreeLineAvatarIconListItem:
    markup: True
    text: "12:00"
    font_style: "H5"
    secondary_text: "Test of Friday!"
    tertiary_text: ", ".join(["Sun", "Mon", "Tue", "Wen", "Thu"])
    tertiary_font_style: "Subtitle2"
    on_release: print("Clicked item")
    

    IconLeftWidget:
        icon: "pencil"
        on_release: print("Clicked edit")

    IconRightWidget:
        icon: "delete"
        on_release: print("Clicked delete")
"""