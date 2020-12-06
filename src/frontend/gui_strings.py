screen_helper = """
ScreenManager:
    # MainScreen:
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
            right_action_items: [["plus", lambda x: root.add_alarm()]]


        ScrollView:
            id: scroll
            MDList:
                id: list

<AlarmFormScreen>:
    name: 'alarm_form'

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
            icon: "clock"
            text: "12:00"
            font_size: '70sp'
            height: dp(60)
            width: dp(250)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}


        MDBoxLayout:
            orientation:'horizontal'
            id: "alarm_from_days_box"
            padding: [20,20,20,20]
            size_hint_y: .2

            MDBoxLayout:
                id: "alarm_from_day_mon"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Mon"

                MDCheckbox:

            MDBoxLayout:
                id: "alarm_from_day_tue"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Tue"

                MDCheckbox:

            MDBoxLayout:
                id: "alarm_from_day_wen"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Wen"

                MDCheckbox:

            MDBoxLayout:
                id: "alarm_from_day_thu"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Thu"

                MDCheckbox:

            MDBoxLayout:
                id: "alarm_from_day_fri"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Fri"
                
                MDCheckbox:
                    active: True

            MDBoxLayout:
                id: "alarm_from_day_sat"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Sat"

                MDCheckbox:

            MDBoxLayout:
                id: "alarm_from_day_sun"
                orientation:'vertical'

                MDLabel:
                    halign: "center"
                    valign: "center"
                    text: "Sun"

                MDCheckbox:

        MDBoxLayout:
            orientation:'vertical'
            id: "alarm_form_types_box"
            size_hint_y: .2

            MDBoxLayout:
                orientation:'horizontal'
                id: "alarm_from_types_checkboxes"

                MDBoxLayout:
                    orientation:'vertical'
                    id: "type_speech_box"

                    MDLabel:
                        halign: "center"
                        valign: "center"
                        text: "Speech"

                    MDCheckbox:
                        group: 'types'

                MDBoxLayout:
                    orientation:'vertical'
                    id: "type_face_box"

                    MDLabel:
                        halign: "center"
                        valign: "center"
                        text: "Face"

                    MDCheckbox:
                        group: 'types'

                MDBoxLayout:
                    orientation:'vertical'
                    id: "type_none_box"

                    MDLabel:
                        halign: "center"
                        valign: "center"
                        text: "None"

                    MDCheckbox:
                        active: True
                        group: 'types'
                
        MDTextField:
            size_hint_x: .5
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            hint_text: "Staring Time (Seconds)"
            disabled: True

    MDToolbar:
        pos_hint: {"bottom": 1}
        elevation: 11
        right_action_items: [["check", lambda x: print("add alarm")]]
        left_action_items: [["close", lambda x: print("cancel alarm")]]


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