#!/usr/bin/env python3
# coding: utf-8

# stdlibs
import json
import argparse
import getpass
import datetime

# dependencies
import requests
import matplotlib.pyplot as plt
import numpy as np

ARGOAPI_URL = 'https://www.portaleargo.it/famiglia/api/rest/'
ARGOAPI_KEY = 'ax6542sdru3217t4eesd9'
ARGOAPI_VERSION = '2.0.2'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
TOGGLE = False

def onpick(event):
	fig, lines, lined, legline, origline = get_graph.fig, get_graph.lines, get_graph.lined, get_graph.legline, get_graph.origline
	legline = event.artist
	origline = lined[legline]
	vis = not origline.get_visible()
	origline.set_visible(vis)
	
	if vis:
		legline.set_alpha(1.0)
	else:
		legline.set_alpha(0.2)

	fig.canvas.draw()

def onclick(event):
	fig, lines, lined, legline, origline = get_graph.fig, get_graph.lines, get_graph.lined, get_graph.legline, get_graph.origline
	global TOGGLE

	if event.button == 3:
		for origline in lines:
			origline.set_visible(TOGGLE)

		for legline in lined:
			if TOGGLE:
				legline.set_alpha(1.0)
			else:
				legline.set_alpha(0.2)

	TOGGLE = not TOGGLE

	fig.canvas.draw()

def get_graph():
	avg_all, marks_tot = 0, 0
	date_all, lines = [], []
	marks_dict, lined = {}, {}
	time_delta, api_response = datetime.timedelta(days = 3), get_marks()

	if not args.file and not args.big:
		fig = plt.figure(figsize = (12.4, 5))
		ax = fig.add_subplot(1, 1, 1)
	else:
		fig = plt.figure(figsize = (18, 10))
		ax = fig.add_subplot(1, 1, 1)

	plt.gcf().canvas.set_window_title('Grafico Voti')
	plt.grid(which = 'both')
	major_ticks = np.arange(0, 11, 1)
	minor_ticks = np.arange(0, 11, 0.5)
	ax.set_yticks(major_ticks)
	ax.set_yticks(minor_ticks, minor = True)
	ax.grid(which = 'major', alpha = 0.5)
	ax.grid(which = 'minor', alpha = 0.2)

	for vote in api_response['dati']:
		if vote.get('desMateria') and vote['decValore'] and vote['datGiorno']:
			if marks_dict.get(vote['desMateria']):
				marks_dict[vote['desMateria']][0].append(vote['decValore'])
				marks_dict[vote['desMateria']][1].append(vote['datGiorno'])
			else:
				marks_dict[vote['desMateria']] = [vote['decValore']], [vote['datGiorno']]

	for subj in marks_dict:
		avg_subj, date_subj = 0, []

		for day in marks_dict[subj][1]:
			date_subj.append(datetime.datetime.strptime(day, '%Y-%m-%d'))
			date_all.append(datetime.datetime.strptime(day, '%Y-%m-%d'))

		for v in marks_dict[subj][0]:
			avg_subj += v
			avg_all += v

		tmp, = ax.plot(date_subj[::-1], marks_dict[subj][0][::-1], label = subj, marker = 'o', alpha = 0.9)
		lines.append(tmp)

		marks_tot += len(marks_dict[subj][0])
	
		if args.verbose:
			print(subj + ': ' + str(' - '.join(str(x) for x in marks_dict[subj][0][::-1])))
			print('Media: ' + str(round(avg_subj / len(marks_dict[subj][0]), 2)), end='\n\n')

	avg_all /= marks_tot

	if args.verbose:
		print('La tua Media totale e\':', round(avg_all, 2))

	ax.axis([sorted(date_all)[0] - time_delta, sorted(date_all)[-1] + time_delta, 0, 10.1])
	lines.append(ax.axhline(y = avg_all, alpha = 0.2, color = 'g', linestyle = '-', label = 'Media', linewidth = 3))
	ax.axhline(y = 6, alpha = 0.2, color = 'r', linestyle = '--', label = 'Sufficienza', linewidth = 3)
	
	if args.file or args.big:
		leg = ax.legend(loc = 4)
		leg.get_frame().set_alpha(0.4)

		for legline, origline in zip(leg.get_lines(), lines):
			legline.set_picker(5) 
			lined[legline] = origline

		fig.subplots_adjust(left = 0.02, right = 0.98, top = 0.98, bottom = 0.05)

		if args.file:
			fig.savefig(args.file + '.png' if not args.file.endswith('.png') else args.file, format = 'png', dpi = 300)
			print('Grafico salvato nel file ' + args.file + ('.png' if not args.file.endswith('.png') else ''))

		if args.big:
			get_graph.fig, get_graph.lines, get_graph.lined, get_graph.legline, get_graph.origline = fig, lines, lined, legline, origline
			fig.canvas.mpl_connect('pick_event', onpick)
			fig.canvas.mpl_connect('button_press_event', onclick)
			plt.show()
	else:
		leg = ax.legend(bbox_to_anchor = (1, 1), loc = "upper left", prop = {'size': 8})
		leg.get_frame().set_alpha(0.4)

		for legline, origline in zip(leg.get_lines(), lines):
			legline.set_picker(5) 
			lined[legline] = origline

		fig.subplots_adjust(left = 0.02, right = 0.7, top = 0.98, bottom = 0.05)
		get_graph.fig, get_graph.lines, get_graph.lined, get_graph.legline, get_graph.origline = fig, lines, lined, legline, origline
		fig.canvas.mpl_connect('pick_event', onpick)
		fig.canvas.mpl_connect('button_press_event', onclick)
		plt.show()

def get_marks():
	base_header = {'x-cod-min': SCHOOL_CODE, 'x-key-app': ARGOAPI_KEY, 'x-version': ARGOAPI_VERSION, 'user-agent': USER_AGENT}
	loginheader = {'x-user-id': USERNAME, 'x-pwd': PASSWORD}
	loginheader.update(base_header)
	token = json.loads(request('login', loginheader))['token']
	token_header = {'x-auth-token': token}
	token_header.update(base_header)
	userdata = json.loads(request('schede', token_header))[0]
	base_header = token_header
	data_header = dict({'x-prg-alunno': str(userdata['prgAlunno']), 'x-prg-scheda': str(userdata['prgScheda']), 'x-prg-scuola': str(userdata['prgScuola'])})
	data_header.update(base_header)

	return json.loads(request('votigiornalieri', data_header))

def request(page, header):
	r = requests.get(
		url = ARGOAPI_URL + page,
		headers = header,
	)

	if r.status_code != requests.codes.ok:
		print('ERRORE:', r.status_code)
		raise ConnectionRefusedError()

	return r.text


if __name__ == '__main__':
	c = 1
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--school')
	parser.add_argument('-u', '--username')
	parser.add_argument('-p', '--password')
	parser.add_argument('-f', '--file')
	parser.add_argument('-b', '--big', action='store_true')
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	SCHOOL_CODE = input('Codice Scuola: ') if not args.school else args.school
	
	while c:
		USERNAME = input('Username: ') if not args.username else args.username if c == 1 else input('Username: ')
		PASSWORD = getpass.getpass('Password: ') if not args.password else args.password if c == 1 else getpass.getpass('Password: ')
		try:
			get_graph()
			c = 0
		except:
			print('Credenziali Errate', end = '\n\n')
			c += 1
