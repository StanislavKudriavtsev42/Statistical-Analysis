from tkinter import messagebox

from nltk import tokenize
import locale
import matplotlib.pyplot as plt
from tkinter import *


def PlotGraph(x, y, x_axis_name, y_axis_name, graph_name, xticks = plt.xticks()):
    plt.xticks(x, xticks)
    plt.plot(x, y, marker='o')
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.title(graph_name)
    plt.show()

class FileManager:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "r", encoding='UTF-8')

    def GetFileString(self):
        return self.file.read().replace('\n', " ")

class TextProcessor:
    def __init__(self, text, language):
        self.ger_alphabet_list = {'a': 0, 'ä': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0,
                         'l': 0, 'm': 0, 'n': 0, 'o': 0, 'ö': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 'ß': 0, 't': 0, 'u': 0,
                         'ü': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

        self.rom_alphabet_list = {'a': 0, 'ă': 0, 'â': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'î': 0,
                         'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 'ș': 0, 't': 0,
                         'ț': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

        self.hun_alphabet_list = {'a': 0, 'á': 0, 'b': 0, 'c': 0, 'cs': 0, 'd': 0, 'dz': 0, 'dzs': 0, 'e': 0, 'é': 0, 'f': 0, 'g': 0,
                         'gy': 0, 'h': 0, 'i': 0, 'í': 0, 'j': 0, 'k': 0, 'l': 0, 'ly': 0, 'm': 0, 'n': 0, 'ny': 0, 'o': 0,
                         'ó': 0, 'ö': 0, 'ő': 0,'p': 0, 'q': 0, 'r': 0, 's': 0, 'sz': 0, 't': 0, 'ty': 0, 'u': 0, 'ú': 0,
                         'ü': 0, 'ű': 0,'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0, 'zs': 0}

        self.ua_alphabet_list = {'а': 0, 'б': 0, 'в': 0, 'г': 0, 'ґ': 0, 'д': 0, 'е': 0, 'є': 0, 'ж': 0, 'з': 0, 'и': 0, 'і': 0,
                        'ї': 0, 'й': 0, 'к': 0, 'л': 0, 'м': 0, 'н': 0, 'о': 0, 'п': 0, 'р': 0, 'с': 0, 'т': 0, 'у': 0,
                        'ф': 0, 'х': 0, 'ц': 0, 'ч': 0, 'ш': 0, 'щ': 0, 'ь': 0, 'ю': 0, 'я': 0}

        self.rus_alphabet_list = {'а': 0, 'б': 0, 'в': 0, 'г': 0, 'д': 0, 'е': 0, 'ё': 0, 'ж': 0, 'з': 0, 'и': 0, 'й': 0, 'к': 0,
                         'л': 0, 'м': 0, 'н': 0, 'о': 0, 'п': 0, 'р': 0, 'с': 0, 'т': 0, 'у': 0, 'ф': 0, 'х': 0, 'ц': 0,
                         'ч': 0, 'ш': 0, 'щ': 0, 'ъ': 0, 'ы': 0, 'ь': 0, 'э': 0,'ю': 0, 'я': 0}

        self.alphabets = {"українська": self.ua_alphabet_list, "російська": self.rus_alphabet_list, "німецька": self.ger_alphabet_list,
                          "угорська": self.hun_alphabet_list, "румунська": self.rom_alphabet_list}
        self.language = language
        self.text_contains_unregistered_characters = False
        self.word_lengths = {}
        self.sentence_lengths = {}
        self.textbox_text = ""

        self.text = text

    def Initiate(self):
        self.words = self.SplitTextByWords(self.text)
        self.sentences = self.SplitTextBySentences(self.text)
        self.CountLetters()
        self.CountWordLengths()

    def SplitTextByWords(self, text):
        characters_to_replace = "?!,.…–():;’\"«»[]—•“”1234567890²"
        for char in characters_to_replace:
            text = text.replace(char, " ")
        return text.split()

    def SplitTextBySentences(self, text):
        return tokenize.sent_tokenize(text)

    def CountLetters(self):
        digraph = ""
        use_digraphs = False
        self.text_contains_unregistered_characters = False
        used_alphabet = self.alphabets[self.language]
        valid_letters = used_alphabet.keys()

        if self.language == "угорська":
            use_digraphs = True

        for alphabet in self.alphabets:
            for key in self.alphabets[alphabet]:
                self.alphabets[alphabet][key] = 0

        for word in self.words:
            word = word.lower()
            for letter in word:
                if letter == "'" or letter == "-":
                    digraph = ""
                    continue

                if use_digraphs:
                    digraph += letter
                else:
                    if valid_letters.__contains__(letter):
                        used_alphabet[letter] += 1
                    else:
                        self.text_contains_unregistered_characters = True
                    continue

                if digraph.__len__() == 3:
                    if valid_letters.__contains__(digraph):
                        used_alphabet[digraph] += 1
                    elif valid_letters.__contains__(digraph[:-1]):
                        used_alphabet[digraph[:-1]] += 1
                    elif valid_letters.__contains__(digraph[1:]):
                        used_alphabet[digraph[1:]] += 1
                    else:
                        if valid_letters.__contains__(digraph[0]):
                            used_alphabet[digraph[0]] += 1
                        else:
                            self.text_contains_unregistered_characters = True
                        if valid_letters.__contains__(digraph[1]):
                            used_alphabet[digraph[1]] += 1
                        else:
                            self.text_contains_unregistered_characters = True
                        if valid_letters.__contains__(digraph[2]):
                            used_alphabet[digraph[2]] += 1
                        else:
                            self.text_contains_unregistered_characters = True
                    digraph = ""

            if self.word_lengths.__contains__(word.__len__()):
                self.word_lengths[word.__len__()] += 1
            else:
                self.word_lengths[word.__len__()] = 1

    def CountWordLengths(self):
        for sentence in self.sentences:
            sentence_length = self.SplitTextByWords(sentence).__len__()
            if self.sentence_lengths.__contains__(sentence_length):
                self.sentence_lengths[sentence_length] += 1
            else:
                self.sentence_lengths[sentence_length] = 1
            if self.sentence_lengths.__contains__(0):
                del self.sentence_lengths[0]

    def SubstringCount(self, substring):
        return self.text.lower().count(substring.lower())

    def SubstringSplit(self, characters_string):
        characters = characters_string.split()
        characters = dict.fromkeys(characters)
        for character in characters:
            if character.__len__() < 2 or character.__len__() > 5:
                return {0: 0}
            characters[character] = self.SubstringCount(character)
        if not bool(characters):
            return {0: 0}
        return characters

    def SortWords(self):
        sorted_words = []
        for word in self.words:
            sorted_words.append(word.lower())
        locale.setlocale(locale.LC_ALL, "")
        sorted_words.sort(key=locale.strxfrm)
        return sorted_words

    def CountSortedWords(self):
        sorted_words = self.SortWords()
        sorted_words_count = {}
        for word in sorted_words:
            if not sorted_words_count.__contains__(word):
                sorted_words_count[word] = sorted_words.count(word)
                print(word + ": " + str(sorted_words_count[word]))
        if sorted_words_count.keys().__contains__("-"):
            del sorted_words_count["-"]
        return sorted_words_count


class DialogWindow:
    def __init__(self, root, rows, columns, graph_name):
        self.root = root

        top = Toplevel(root)

        keys = rows
        frequency = columns

        volume = float(sum(frequency))
        relative_frequency = []
        relative_frequency_table = []
        for value in frequency:
            if value != 0:
                relative_frequency.append(float('%.3f' % (value / volume)))
                relative_frequency_table.append(float('%.2f' % (value / volume)))
            else:
                relative_frequency.append(0)
                relative_frequency_table.append(0)

        menubar = Menu(self.root)
        graph_menu = Menu(menubar)
        graph_menu.add_command(label="Частота", command=lambda: self.DrawGraph(keys, frequency, "Xi", "Ni", graph_name))
        graph_menu.add_command(label="Відносна частота", command=lambda: self.DrawGraph(keys, relative_frequency, "Xi", "Wi", graph_name))
        menubar.add_cascade(label="Графічна характеристика", menu=graph_menu)
        top.config(menu=menubar)

        keys_table = keys.copy()
        keys_table.insert(0, " ")
        frequency_table = frequency.copy()
        frequency_table.insert(0, "ni")
        relative_frequency_table.insert(0, "wi")
        width = keys_table.__len__()
        height = 3

        row_shift = 0
        column_coef = 0
        for i in range(height):  # Rows
            for j in range(width):  # Columns
                if j > 30 and row_shift == 0:
                    row_shift += 3
                    column_coef = j - 1
                if i == 0:
                    label = Label(top, width=5, borderwidth = 1, relief="sunken", text=keys_table[j], font=("Helvetica", 12))
                elif i == 1:
                    label = Label(top, width=5, borderwidth = 1,relief="sunken", text=frequency_table[j], font=("Helvetica", 12))
                elif i == 2:
                    label_text = relative_frequency_table[j]
                    label = Label(top, width=5, borderwidth = 1,relief="sunken", text=label_text, font=("Helvetica", 12))
                label.grid(row=i + row_shift, column=j - column_coef)
            row_shift = 0
            column_coef = 0

    def DrawGraph(self, keys, values, x_axis, y_axis, name):
        x = range(1, keys.__len__() + 1)
        y = values

        ticks = []
        for key in keys:
            ticks.append(key)
        PlotGraph(x, y, x_axis, y_axis, name, xticks=ticks)

class TextDisplay:
    def __init__(self, root, frequncy_dictionary, header):
        self.root = root
        self.top = Toplevel(root)

        self.text_box = Text(self.top)
        self.text_box.grid(row=0, column=0)
        scrollb = Scrollbar(self.top, command=self.text_box.yview)
        scrollb.grid(row=0, column=1, sticky="nesw")
        self.text_box['yscrollcommand'] = scrollb.set

        self.text_box.insert('end', header)
        for key in frequncy_dictionary:
            line = key + " -     Ni: " + str(frequncy_dictionary[key]) + "     Wi: " + \
                   str('%.4f' % (frequncy_dictionary[key] / frequncy_dictionary.__len__())) + "\n"
            self.text_box.insert('end', line)
        self.text_box.configure(state=DISABLED)

class TextInputWindow:
    def __init__(self, root, button_text, tp, text, message_label, mb):
        self.root = root
        self.tp = tp
        self.message_label = message_label
        self.main_menubar = mb
        self.top = Toplevel(root)
        self.top.geometry('400x75+40+40')

        self.menubar = Menu(self.top)
        self.menubar.add_command(label=button_text, command=lambda: self.CheckInput(self.text_box.get("1.0", END)))
        self.top.config(menu=self.menubar)

        self.text_box = Text(self.top)
        self.text_box.pack()
        self.text_box.delete(1.0, "end")
        self.text_box.insert(1.0, text)


    def CheckInput(self, input):
        self.tp.text = input
        self.tp.Initiate()
        self.tp.textbox_text = self.text_box.get("1.0", END)
        self.message_label["text"] = "Дані введені користувачем було збережено"
        self.main_menubar.entryconfig("Алфавіт", state=NORMAL)
        self.main_menubar.entryconfig("Слова", state=NORMAL)
        self.main_menubar.entryconfig("Речення", state=NORMAL)
        self.main_menubar.entryconfig("Буквосполучення", state=NORMAL)
        self.main_menubar.entryconfig("Відсортувати", state=NORMAL)
        self.top.destroy()

class StringInputWindow:
    def __init__(self, root, message, button_text, tp):
        self.root = root
        self.top = Toplevel(root)
        self.tp = tp
        self.top.geometry('400x75+40+40')

        self.label = Label(self.top, text=message)
        self.label.pack()
        self.entry = Entry(self.top)
        self.entry.pack()
        self.button = Button(self.top, text=button_text, command=lambda: self.CheckInput(self.entry.get()))
        self.button.pack()

    def CheckInput(self, string):
        responce = self.tp.SubstringSplit(string)
        if 0 in responce:
            messagebox.showerror(title="Помилка", message="Рядок містить буквосполучення < 2 або > 5")
            return
        else:
            rows = []
            columns = []
            for key in responce:
                rows.append(key)
                columns.append(responce[key])
            DialogWindow(self.root, rows, columns, "Буквосполучення")

    def close_app(self):
        self.top.destroy()

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('500x170+40+40')
        self.root.protocol('WM_DELETE_WINDOW', self.close_app)
        self.CreateMainMenu()
        self.text_processor = None

        Label(self.root, text="Введіть назву та розширення файлу:").pack()
        entry = Entry(self.root)
        entry.pack()
        Button(self.root, text="Відкрити", command=lambda: self.OpenFile(entry.get())).pack()
        self.message_label = Label(self.root, text="")
        self.message_label.pack()

        Label(self.root, text="Виберіть мову тексту:").pack()
        self.language = StringVar(self.root)
        self.language.set("українська")
        dropdown = OptionMenu(self.root, self.language, "українська", "російська", "німецька", "угорська", "румунська")
        dropdown.pack()
        self.input_button = Button(self.root, text="Ввести текст вручну", command=self.UserTextInput)
        self.input_button.pack()

        self.root.mainloop()

    def close_app(self):
        exit()

    def CreateMainMenu(self):
        self.menubar = Menu(self.root)
        self.menubar.add_command(label="Алфавіт", command=self.DisplayLetters)
        self.menubar.add_command(label="Слова", command=self.DisplayWords)
        self.menubar.add_command(label="Речення", command=self.DisplaySentences)
        self.menubar.add_command(label="Буквосполучення", command=self.DisplayCharacters)
        self.menubar.add_command(label="Відсортувати", command=self.DisplaySorted)
        self.LockMenu()
        self.root.config(menu=self.menubar)

    def DisplayLetters(self):
        self.text_processor.language = self.language.get()
        self.text_processor.CountLetters()
        if(self.text_processor.text_contains_unregistered_characters):
            messagebox.showerror(title="Помилка", message="Було вибрано неправельний алфавіт, або в тексті присутні декілька мов")
            return
        rows = []
        used_alphabet = self.text_processor.alphabets[self.language.get()]
        self.text_processor.language = self.language.get()
        self.text_processor.CountLetters()
        for row in list(used_alphabet.keys()):
            rows.append(row.upper())
        columns = list(used_alphabet.values())
        DialogWindow(self.root, rows, columns, "Алфавіт")

    def DisplayWords(self):
        if (self.text_processor.text_contains_unregistered_characters):
            messagebox.showerror(title="Помилка", message="Було вибрано неправельний алфавіт, або в тексті присутні декілька мов")
            return
        rows = []
        columns = []
        for key in sorted(self.text_processor.word_lengths):
            rows.append(key)
            columns.append(self.text_processor.word_lengths[key])
        DialogWindow(self.root, rows, columns, "Слова")

    def DisplaySentences(self):
        rows = []
        columns = []
        for key in sorted(self.text_processor.sentence_lengths):
            rows.append(key)
            columns.append(self.text_processor.sentence_lengths[key])
        DialogWindow(self.root, rows, columns, "Речення")

    def DisplayCharacters(self):
        StringInputWindow(self.root, "Введіть буквосполучення (2 <= n <= 5 символи) через пробіл:", "Ввести", self.text_processor)

    def DisplaySorted(self):
        sorted_words = self.text_processor.CountSortedWords()
        header = "---Загальна кількість слів: " + str(self.text_processor.words.__len__()) + "---\n"
        TextDisplay(self.root, sorted_words, header)

    def OpenFile(self, name):
        try:
            self.file_manager = FileManager(name)
            self.text_processor = TextProcessor(self.file_manager.GetFileString(), self.language.get())
            self.text_processor.Initiate()
        except FileNotFoundError:
            self.message_label['text'] = "Такого файлу не існує або його розширення не підтримується"
            self.LockMenu()
            return
        self.message_label['text'] = "Файл '" + name + "' відкрито"
        self.UnlockMenu()

    def UserTextInput(self):
        textbox_text = ""
        if self.text_processor is not None:
            textbox_text = self.text_processor.textbox_text
        self.text_processor = TextProcessor("", self.language.get())
        TextInputWindow(self.root, "Зберегти", self.text_processor, textbox_text, self.message_label, self.menubar)

    def LockMenu(self):
        self.menubar.entryconfig("Алфавіт", state=DISABLED)
        self.menubar.entryconfig("Слова", state=DISABLED)
        self.menubar.entryconfig("Речення", state=DISABLED)
        self.menubar.entryconfig("Буквосполучення", state=DISABLED)
        self.menubar.entryconfig("Відсортувати", state=DISABLED)

    def UnlockMenu(self):
        self.menubar.entryconfig("Алфавіт", state=NORMAL)
        self.menubar.entryconfig("Слова", state=NORMAL)
        self.menubar.entryconfig("Речення", state=NORMAL)
        self.menubar.entryconfig("Буквосполучення", state=NORMAL)
        self.menubar.entryconfig("Відсортувати", state=NORMAL)

GUI()
