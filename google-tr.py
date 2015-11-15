#!/usr/bin/env python3

from gi.repository import Gtk
from tools import get_resource_path
from tools import get_screen_resolution
from tools import get_selected_text
from tools import get_translate

trn_lang = 'ru'
languages = [
    ['af', 'Afrikaans'],
    ['sq', 'Albanian'],
    ['ar', 'Arabic'],
    ['hy', 'Armenian'],
    ['az', 'Azerbaijani'],
    ['eu', 'Basque'],
    ['be', 'Belarusian'],
    ['bn', 'Bengali'],
    ['bs', 'Bosnian'],
    ['bg', 'Bulgarian'],
    ['ca', 'Catalan'],
    ['ceb', 'Cebuano'],
    ['ny', 'Chichewa'],
    ['zh-CN"', 'Chinese'],
    ['hr', 'Croatian'],
    ['cs', 'Czech'],
    ['da', 'Danish'],
    ['auto', 'Detect language'],
    ['nl', 'Dutch'],
    ['en', 'English'],
    ['eo', 'Esperanto'],
    ['et', 'Estonian'],
    ['tl', 'Filipino'],
    ['fi', 'Finnish'],
    ['fr', 'French'],
    ['gl', 'Galician'],
    ['ka', 'Georgian'],
    ['de', 'German'],
    ['el', 'Greek'],
    ['gu', 'Gujarati'],
    ['ht', 'Haitian Creole'],
    ['ha', 'Hausa'],
    ['iw', 'Hebrew'],
    ['hi', 'Hindi'],
    ['hmn', 'Hmong'],
    ['hu', 'Hungarian'],
    ['is', 'Icelandic'],
    ['ig', 'Igbo'],
    ['id', 'Indonesian'],
    ['ga', 'Irish'],
    ['it', 'Italian'],
    ['ja', 'Japanese'],
    ['jw', 'Javanese'],
    ['kn', 'Kannada'],
    ['kk', 'Kazakh'],
    ['km', 'Khmer'],
    ['ko', 'Korean'],
    ['lo', 'Lao'],
    ['la', 'Latin'],
    ['lv', 'Latvian'],
    ['lt', 'Lithuanian'],
    ['mk', 'Macedonian'],
    ['mg', 'Malagasy'],
    ['ms', 'Malay'],
    ['ml', 'Malayalam'],
    ['mt', 'Maltese'],
    ['mi', 'Maori'],
    ['mr', 'Marathi'],
    ['mn', 'Mongolian'],
    ['my', 'Myanmar (Burmese)'],
    ['ne', 'Nepali'],
    ['no', 'Norwegian'],
    ['fa', 'Persian'],
    ['pl', 'Polish'],
    ['pt', 'Portuguese'],
    ['pa', 'Punjabi'],
    ['ro', 'Romanian'],
    ['ru', 'Russian'],
    ['sr', 'Serbian'],
    ['st', 'Sesotho'],
    ['si', 'Sinhala'],
    ['sk', 'Slovak'],
    ['sl', 'Slovenian'],
    ['so', 'Somali'],
    ['es', 'Spanish'],
    ['su', 'Sundanese'],
    ['sw', 'Swahili'],
    ['sv', 'Swedish'],
    ['tg', 'Tajik'],
    ['ta', 'Tamil'],
    ['te', 'Telugu'],
    ['th', 'Thai'],
    ['tr', 'Turkish'],
    ['uk', 'Ukrainian'],
    ['ur', 'Urdu'],
    ['uz', 'Uzbek'],
    ['vi', 'Vietnamese'],
    ['cy', 'Welsh'],
    ['yi', 'Yiddish'],
    ['yo', 'Yoruba'],
    ['zu', 'Zulu']
]


class GoogleTranslate:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui.glade")
        self.win = builder.get_object("window")
        """ :type: Gtk.Window """
        self.win.set_title('Google Translate')
        self.win.set_icon_from_file(get_resource_path('icon.png'))
        self.src_lang_combo = builder.get_object("src_lang")
        """ :type: Gtk.ComboBoxText """
        self.trn_lang_combo = builder.get_object("trn_lang")
        """ :type: Gtk.ComboBoxText """
        self.src_text = builder.get_object("src_text")
        """ :type: Gtk.TextView """
        self.trn_text = builder.get_object("trn_text")
        """ :type: Gtk.TextView """
        self.src_listen_btn = builder.get_object("src_listen_btn")
        """ :type: Gtk.Button """
        self.trn_listen_btn = builder.get_object("trn_listen_btn")
        """ :type: Gtk.Button """
        self.close_btn = builder.get_object("close")
        """ :type: Gtk.Button """
        self.spinner = builder.get_object("spinner")
        """ :type: Gtk.Spinner """
        for lang in languages:
            self.src_lang_combo.append(lang[0], lang[1])
            if lang[0] != 'auto':
                self.trn_lang_combo.append(lang[0], lang[1])
        self.src_lang_combo.set_active_id('auto')
        self.trn_lang_combo.set_active_id(trn_lang)

        self.src_listen_btn.connect("clicked", self.on_button_clicked)
        self.close_btn.connect("clicked", self.on_close_clicked)
        # self.win.set_keep_above(True)
        self.win.show()
        width = self.win.get_border_width() + self.win.get_allocated_width()
        if width > 0:
            self.win.move(get_screen_resolution('width') - width, 0)
        self.win.set_keep_above(True)
        self.start_translate()

    def start_translate(self):
        self.set_sensitive(False)
        orig = get_selected_text()
        if len(orig) > 0:
            response = get_translate(orig, 'auto', trn_lang)
            if 'sentences' in response and 'trans' in response['sentences'][0]:
                trans = response['sentences'][0]['trans']
                # trans = str(trans, encoding='UTF-8')
                orig = response['sentences'][0]['orig']
                # orig = str(orig, encoding='UTF-8')
                src = response['src']
            else:
                trans = ''
                src = 'auto'

            print(trans)

            self.src_text.get_buffer().set_text(orig)
            self.trn_text.get_buffer().set_text(trans)
            self.src_lang_combo.set_active_id(src)
        self.set_sensitive(True)

    def set_sensitive(self, status):
        """ :param bool status: """
        self.src_lang_combo.set_sensitive(status)
        self.trn_lang_combo.set_sensitive(status)
        self.src_listen_btn.set_sensitive(status)
        self.trn_listen_btn.set_sensitive(status)
        self.src_text.set_visible(status)
        self.trn_text.set_visible(status)
        self.spinner.stop() if status else self.spinner.start()

    def on_button_clicked(self, widget):
        print('clicked')

    def on_close_clicked(self, widget):
        self.win.close()
        exit()


if __name__ == "__main__":
    GoogleTranslate()
    Gtk.main()
