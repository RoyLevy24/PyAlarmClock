# This file contains Strings written in KV language
# The Strings will be used for creating elements such as the Screens of the application.


screen_helper = """
ScreenManager:
    MainScreen:
    AlarmFormScreen:
    AlarmActiveScreen:
    DismissSpeechScreen:



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

    form_toolbar: form_toolbar
    time_picker: time_picker
    check_days: [check_mon, check_tue, check_wen, check_thu, check_fri, check_sat, check_sun]
    tf_alarm_param: tf_alarm_param
    check_type: [check_speech, check_face, check_none]
    alarm_desc: alarm_desc

    MDToolbar:
        id: form_toolbar
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

    alarm_active_time: alarm_active_time 
    alarm_active_desc: alarm_active_desc
    alarm_active_dismiss: alarm_active_dismiss
    MDToolbar:
        title: "Alarm Active"
        pos_hint: {"top": 1}
        elevation: 11

    MDBoxLayout:
        id: alarm_active_box
        orientation: 'vertical'
        size_hint_y: .5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: [20,20,20,20]

        MDLabel:
            id: alarm_active_time
            halign: "center"
            valign: "center"
            markup: True
            font_style: "H1"

        MDLabel:
            id: alarm_active_desc
            halign: "center"
            valign: "center"
            markup: True
            multiline: True
            font_style: "H6"

        Label:

        MDFillRoundFlatButton:
            id: alarm_active_dismiss
            text: "dismiss"
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            font_size: '40sp'
            size_hint_y: 0.9

<DismissSpeechScreen>
    name: 'dismiss_speech'

    dismiss_speech_title: dismiss_speech_title
    dismiss_speech_word: dismiss_speech_word
    dismiss_speech_pronounce: dismiss_speech_pronounce
    dismiss_speech_play_word: dismiss_speech_play_word
    dismiss_speech_pos: dismiss_speech_pos
    dismiss_speech_word_desc: dismiss_speech_word_desc
    dismiss_speech_record: dismiss_speech_record
    dismiss_speech_bottom: dismiss_speech_bottom
    MDToolbar:
        id: dismiss_speech_title
        pos_hint: {"top": 1}
        elevation: 11
        
    MDBoxLayout:
        orientation: 'vertical'
        padding: [20,20,20,20]
        spacing: 5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: .7
        
        MDLabel:
            id: dismiss_speech_word
            halign: "center"
            valign: "center"
            markup: True
            font_style: "H4"
            

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                id: dismiss_speech_pronounce
                halign: "center"
                valign: "center"
                markup: True
                font_style: "H6"
            
            MDIconButton:
                id: dismiss_speech_play_word
                icon: "play-circle"
                size_hint_y: .3
                size_hint_x: .6
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        MDLabel:
            id: dismiss_speech_pos
            markup: True
            font_style: "H6"
            font_name: "Roboto-Italic"

        MDLabel:
            id: dismiss_speech_word_desc
            multiline: True

        MDFloatingActionButton:
            id: dismiss_speech_record
            icon: "microphone"
            elevation_normal: 10
            md_bg_color: app.theme_cls.primary_light
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    MDToolbar:
        id: dismiss_speech_bottom
        title: "Next Word"
        pos_hint: {"bottom": 1}

"""


alarm_string = """
ThreeLineAvatarIconListItem:
    markup: True
    font_style: "H5"
    tertiary_font_style: "Subtitle2"  

    IconLeftWidget:
        icon: "pencil"
        on_release: app.root.screens[0].edit_alarm(root.name)

    IconRightWidget:
        icon: "delete"
        on_release: app.root.screens[0].show_delete_alarm_dialog(root.name)
"""
