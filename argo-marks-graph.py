#!/usr/bin/env python3
# coding: utf-8

# stdlibs
import json
import argparse
import getpass
import datetime

# dependencies
import argoscuolanext
import matplotlib.pyplot as plt
import numpy as np

def new_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--school')
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('-f', '--file')
    parser.add_argument('-b', '--big', action='store_true')
    parser.add_argument('-n', '--not-counted', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--load')
    parser.add_argument('--save', action='store_true')

    return parser.parse_args()

class ArgoGraph(object):
    def __init__(self, username = None, password = None, school_code = None, args = None):
        self.USERNAME = username
        self.PASSWORD = password
        self.SCHOOL_CODE = school_code
        self.TOGGLE = False
        self.args = args
        self.loadDicts()
        self.getGraph()

    def toFile(self):
        try:
            f = open(self.USERNAME + '.txt', 'w')
            f.write(json.dumps(self.marks_dict, indent=4))
            f.close()
        except:
            raise

    def loadDicts(self):
            if self.args.load:
                try:
                    print('\nCaricando le Statistiche...', end = '\n\n')
                    self.dictionaries = [{'UserName': x, 'Dict': json.loads(open(x, 'r').read())} for x in self.args.load.split(',')]
                except:
                    print('Il file con i voti non e\' presente' if len(self.args.split(',')) == 1 else 'I file con i voti non sono presenti')
                    raise
            else:
                print('\nScaricando le Statistiche...', end = '\n\n')
                self.session = argoscuolanext.Session(self.SCHOOL_CODE, self.USERNAME, self.PASSWORD)
                self.marks_dict = {}

                for vote in self.session.votigiornalieri()['dati']:
                    if (vote.get('desCommento') is not None and ' (non fa media)' not in vote['desCommento']) or self.args.not_counted:
                        if vote.get('desMateria') and vote['decValore'] and vote['datGiorno']:
                            if self.marks_dict.get(vote['desMateria']):
                                self.marks_dict[vote['desMateria']].append({'Voto': vote['decValore'], 'Data': vote['datGiorno']})
                            else:
                                self.marks_dict[vote['desMateria']] = [{'Voto': vote['decValore'], 'Data': vote['datGiorno']}]
                self.dictionaries = [{'UserName': self.USERNAME, 'Dict': self.marks_dict}]

    def getGraph(self):
        dates_list, lines = [], []
        lined = {}
        time_delta = datetime.timedelta(days = 3)

        # Save
        if self.args.save:
            self.toFile()

        # Start Plot Setup
        if not self.args.file and not self.args.big:
            self.fig = plt.figure(figsize = (12.4, 5))
            self.ax = self.fig.add_subplot(1, 1, 1)
        else:
            self.fig = plt.figure(figsize = (18, 10))
            self.ax = self.fig.add_subplot(1, 1, 1)
        plt.gcf().canvas.set_window_title('Grafico Voti')
        plt.grid(which = 'both')
        major_ticks = np.arange(0, 11, 1)
        minor_ticks = np.arange(0, 11, 0.5)
        self.ax.set_yticks(major_ticks)
        self.ax.set_yticks(minor_ticks, minor = True)
        self.ax.grid(which = 'major', alpha = 0.5)
        self.ax.grid(which = 'minor', alpha = 0.2)
        # End Plot Setup

        # Start Plot
        for self.marks_dict in self.dictionaries:
            self.USERNAME = self.marks_dict['UserName']
            self.marks_dict = self.marks_dict['Dict']
            marks_sum, total_marks = 0, 0
            if len(self.dictionaries) > 1:
                color = np.random.rand(3,)

            if self.args.verbose:
                print('Lista voti di {}:'.format(self.USERNAME), end = '\n\n')

            for subj in self.marks_dict:
                if len(self.dictionaries) == 1:
                    color = np.random.rand(3,)
                subj_average_mark = 0

                for mark_dict in self.marks_dict[subj]:
                    mark_dict['Data'] = datetime.datetime.strptime(mark_dict['Data'], '%Y-%m-%d')
                    subj_average_mark += mark_dict['Voto']
                    marks_sum         += mark_dict['Voto']

                marks = list(x['Voto'] for x in self.marks_dict[subj])
                dates = list(x['Data'] for x in self.marks_dict[subj])
                dates_list  += dates
                total_marks += len(marks)

                # Plot, legend
                tmp, = self.ax.plot(dates[::-1], marks[::-1], label = ('{}{}'.format('{}: '.format(self.USERNAME) if len(self.dictionaries) > 1 else '', subj)), marker = 'o', alpha = 0.9, color = color)
                lines.append(tmp)

                if self.args.verbose:
                    print('\t{}: {}'.format(subj, str(' / '.join(str(x) for x in marks[::-1]))))
                    print('\tMedia: {}'.format(str(round(subj_average_mark / len(marks), 2))), end='\n\n')

            marks_sum /= total_marks
            lines.append(self.ax.axhline(y = marks_sum, alpha = 0.2, color = color, linestyle = '-', label = '{}Media'.format('{}: '.format(self.USERNAME) if len(self.dictionaries) > 1 else ''), linewidth = 3))
            if self.args.verbose:
                if self.args.not_counted:
                    print('\t{}, la tua media totale con i voti che non fanno media e\': {}'.format(self.USERNAME, round(marks_sum, 2)), end='\n\n')
                else:
                    print('\t{}, la tua media totale e\': {}'.format(self.USERNAME, round(marks_sum, 2)), end='\n\n')
        # End Plot

        # Axis, Average Line
        self.ax.axis([sorted(dates_list)[0] - time_delta, sorted(dates_list)[-1] + time_delta, 0, 10.1])
        self.ax.axhline(y = 6, alpha = 0.2, color = 'r', linestyle = '--', label = 'Sufficienza', linewidth = 3)

        if self.args.file or self.args.big:
            # Legend
            leg = self.ax.legend(loc = 4)
            leg.get_frame().set_alpha(0.4)

            for legline, origline in zip(leg.get_lines(), lines):
                legline.set_picker(5)
                lined[legline] = origline

            self.fig.subplots_adjust(left = 0.02, right = 0.98, top = 0.98, bottom = 0.05)

            if self.args.file:
                self.fig.savefig(args.file + '.png' if not args.file.endswith('.png') else args.file, format = 'png', dpi = 300)
                print('\nGrafico salvato nel file ' + args.file + ('.png' if not args.file.endswith('.png') else ''))

            if self.args.big:
                self.lines, self.lined, self.legline, self.origline = lines, lined, legline, origline
                self.fig.canvas.mpl_connect('pick_event', self.onPick)
                self.fig.canvas.mpl_connect('button_press_event', self.onClick)
                plt.show()
        else:
            # Legend
            leg = self.ax.legend(bbox_to_anchor = (1, 1), loc = "upper left", prop = {'size': 8})
            leg.get_frame().set_alpha(0.4)

            for legline, origline in zip(leg.get_lines(), lines):
                legline.set_picker(5)
                lined[legline] = origline

            self.fig.subplots_adjust(left = 0.02, right = 0.7, top = 0.98, bottom = 0.05)
            self.lines, self.lined, self.legline, self.origline = lines, lined, legline, origline
            self.fig.canvas.mpl_connect('pick_event', self.onPick)
            self.fig.canvas.mpl_connect('button_press_event', self.onClick)
            plt.show()

    def onPick(self, event):
        self.legline = event.artist
        self.origline = self.lined[self.legline]
        vis = not self.origline.get_visible()
        self.origline.set_visible(vis)
        if vis:
            self.legline.set_alpha(1.0)
        else:
            self.legline.set_alpha(0.2)
        self.fig.canvas.draw()

    def onClick(self, event):
        if event.button == 3:
            for self.origline in self.lines:
                self.origline.set_visible(self.TOGGLE)
            for self.legline in self.lined:
                if self.TOGGLE:
                    self.legline.set_alpha(1.0)
                else:
                    self.legline.set_alpha(0.2)
        self.TOGGLE = not self.TOGGLE
        self.fig.canvas.draw()

if __name__ == '__main__':
    args = new_parser()
    if args.save and args.load:
        print('Non puoi abilitare save e load assieme')
        exit()
    if args.load:
        # File Loading
        ArgoGraph(args = args)
    else:
        # Online Loading
        sc = input('Codice Scuola: ') if not args.school else args.school
        c = 1
        while c:
            usr = input('Username: ') if not args.username else args.username if c == 1 else input('Username: ')
            pw = getpass.getpass('Password: ') if not args.password else args.password if c == 1 else getpass.getpass('Password: ')

            try:
                ArgoGraph(username = usr, password = pw, school_code = sc, args = args)
                c = 0
            # except ConnectionRefusedError as e:
            #     print('Credenziali Errate', e, end = '\n\n')
            #     c += 1
            except Exception as e:
                # print('[Exception]', e)
                print('Credenziali Errate', e, end = '\n\n')
                c += 1
