# -*- coding: utf-8 -*-

from collections import OrderedDict, defaultdict

from stemmer import PorterStemmer
import math
import sys
import argparse
import wx
from wx.lib.wordwrap import wordwrap


def dot_product(vecA, vecB):
    product = 0
    # for a, b in vecA, vecB:
        # product += a * b
    for i in range(len(vecB)):
        product += vecA[i] * vecB[i]
    return product
    
def vec_length(vec):
    length = 0
    for el in vec:
        length += pow(el, 2)
    return math.sqrt(length)
    
        
def vec_similarity(vec1, vec2):
    length_product = vec_length(vec1) * vec_length(vec2)
    if length_product == 0:
        return 0
    else:
        return dot_product(vec1, vec2) / length_product

class TFIDF_Search(object):

    stemmer = PorterStemmer()    
    
    def __init__(self, stopwords_filepath, keywords_filepath, documents_filepath):
        self.keywords = OrderedDict()
        self.documents = defaultdict(list)
        self.stopwords = []
        self.bag_of_words = {}   
        self.documents_count = {}
        self.read_stopwords(stopwords_filepath)
        self.read_keywords(keywords_filepath)
        self.read_documents(documents_filepath)
        self.append_bag_of_words(self.documents)
        
    def clean_word(self, word):
        word = word.lower()
        word = filter(lambda c: c.isalnum(), word)
        if word in self.stopwords:
            return None
        else:
            return self.stemmer.stem(word, 0, len(word)-1)

    def clean_word_list(self, list):
        return [word for word in list if word]

    def read_stopwords(self, stopwords_filepath):
        self.stopwords = []
        with open(stopwords_filepath) as file:
            for line in file:
                self.stopwords.append(line.strip())
        self.stopwords = frozenset(self.stopwords)

    def read_keywords(self, keywords_filepath):
        self.keywords = OrderedDict()
        with open(keywords_filepath) as file:
            for line in file:
                word = line.strip()
                stemmed_word = self.clean_word(word)
                if stemmed_word is not None:
                    self.keywords[stemmed_word] = 0

    #for k in sorted(keywords):
    #    print k

    def read_documents(self, documents_filepath):
        self.documents = defaultdict(list)
        with open(documents_filepath) as file:
            current_doc = None
            for line in file:
                if current_doc is None:
                    current_doc = line.strip()
                words = line.split()
                if words:
                    self.documents[current_doc] += words
                else:
                    current_doc = None

        for k, doc in self.documents.iteritems():
            clean_words = map(self.clean_word, doc)
            self.documents[k] = self.clean_word_list(clean_words)
            
    def append_bag_of_words(self, documents):
        for keyword in self.keywords:
            self.documents_count.setdefault(keyword, 0)
            for k, doc in documents.iteritems():
                keyword_count = doc.count(keyword)
                self.bag_of_words.setdefault(k, {})[keyword] = keyword_count
                if keyword_count > 0:
                    self.documents_count[keyword] += 1
        
        
    def tf(self, document, term):
        n = self.bag_of_words[document][term]
        if n == 0:
            return 0
        else:
            return float(n) / max(self.bag_of_words[document].itervalues())
            
    def idf(self, term):
        if self.documents_count[term] == 0:
            return 0
        else:
            return math.log(len(self.documents) / self.documents_count[term])
        
    def tfidf(self, document):
        result_vector = []
        for term in sorted(self.keywords):
            result_vector.append(self.tf(document, term) * self.idf(term))
        return result_vector

    def similarity(self, doc1, doc2):
        #print "comparing documents: " + doc1 + " " + doc2
        return vec_similarity(self.tfidf(doc1), self.tfidf(doc2))
        
    def search(self, question):
        question_words = question.split()
        question_words_stemmed = []
        for word in question_words:
            word = word.strip()
            stemmed_word = self.clean_word(word)
            if (stemmed_word):    
                question_words_stemmed.append(stemmed_word)
        self.append_bag_of_words({"question" : question_words_stemmed})
        ranking = {}
        for title in self.documents.iterkeys():
            ranking[title] = self.similarity(title, "question")
        
        for title, sim in sorted(ranking.items(), key=(lambda t: t[1]), reverse=True):
            print "%4f\t%s" % (sim, title)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.size = (300,250)
        wx.Frame.__init__(self, parent, title=title, size = self.size )
        
 
        
        self.helpProvider = wx.SimpleHelpProvider()
        wx.HelpProvider.Set(self.helpProvider)
        
        self.openButton = wx.Button(self, label = "Documents File", pos = (10, 10))
        self.openButton.SetHelpText("Choose a file to open")
                
        self.infileLabel = wx.StaticText(self, label = "No file choosen",
					  pos = (self.openButton.GetPosition().x + self.openButton.GetSize().GetWidth() + 10, self.openButton.GetPosition().y)) 
        
        
        
        cBtn = wx.ContextHelpButton(self, pos = (10, 195))
        cBtn.SetHelpText("wx.ContextHelpButton")

        filemenu= wx.Menu()
        helpmenu = wx.Menu()

        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        menuOpen = filemenu.Append(wx.ID_OPEN,"Open"," Open source File")
        menuContextHelp = helpmenu.Append(wx.ID_ANY, "Context help", "Starts context menu mode")
        menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar) 
        
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnContextHelp, menuContextHelp)
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.openButton)
        self.Show(True)

    def OnAbout(self,e):
             
        info = wx.AboutDialogInfo()
        info.Name = "TF-IDF"
        info.Version = "0.3"
        info.Copyright = u"(C) 2011 Krzysztof Urban & Tomasz Ziętkiewicz"
        info.Description = wordwrap(
            "Simple TF-IDF implementation.\nFor command line help run with argument \"-h\"",
            350, wx.ClientDC(self))
        info.WebSite = ("mailto:tomek.zietkiewicz@gmail.com", "Email")
        info.Developers = [ u"Tomasz Ziętkiewicz", "Krzysztof Urban" ]

        info.License = wordwrap("This is free software: you are free to change and redistribute it.\n\nThere is NO WARRANTY, to the extent permitted by law.", 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
    
    def OnContextHelp(self, e):
        contextHelp = wx.ContextHelp()
        contextHelp.BeginContextHelp()
            
        
    def OnOpen(self,e):
      """ Open a file"""
      dirname = ''
      dlg = wx.FileDialog(self, "Choose a source file", dirname, "", "*.*", wx.OPEN)
      if dlg.ShowModal() == wx.ID_OK:
          filename = dlg.GetFilename()
          dirname = dlg.GetDirectory()
          filePath = os.path.join(dirname, filename)
          dlg.Destroy()
    
    def OnExit(self,e):
        self.Close(True)  # Close the frame.
            
            
if __name__ == '__main__':

    if len (sys.argv) == 1 or len(sys.argv) > 1 and (sys.argv[1] == "-g" or sys.argv[1] == "--gui"):
        print "Entered GUI mode"
        app = wx.App(False)
        frame = MainWindow(None, "TF-IDF")
        app.MainLoop()
        sys.exit()
    
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description = "Simple TF-IDF implementation.",
      prog = "enconv",
      epilog = u"Authors:\t\tKrzysztof Urban & Tomasz Ziętkiewicz. 2011\nCopyright:\tThis is free software: you are free to change and redistribute it.\n\t\tThere is NO WARRANTY, to the extent permitted by law."
      )
    parser.add_argument('-k', '--keywords', help="Keywords file path", default="data/keywords.txt")
    parser.add_argument('-s', '--stopwords', help="Stopwords file path", default="data/stopwords.txt")
    parser.add_argument('-d', '--documents', help="Documents file path", default="data/documents.txt")
    parser.add_argument('-g', '--gui', help='GUI mode')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    searcher = TFIDF_Search(args.stopwords, args.keywords, args.documents)
    q = raw_input("Enter search string or \"exit()\" and press enter: ")
    while q != "exit()":
        searcher.search(q)
        q = raw_input("\nEnter search string or \"exit()\" and press enter: ")