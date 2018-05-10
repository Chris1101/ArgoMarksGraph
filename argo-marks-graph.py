import json, requests, argparse, getpass
import matplotlib.pyplot as plt
import numpy as np

def get_graph():
	avg, tot, max1, marks_dict = 0, 0, [], {}
	api_response = get_marks()

	for vote in api_response['dati']:
		if vote['decValore'] and vote.get('desMateria'):
			if marks_dict.get(vote['desMateria']):
				marks_dict[vote['desMateria']].append(vote['decValore'])
			else:
				marks_dict[vote['desMateria']] = [vote['decValore']]
	
	if not args.file:
		ax = plt.figure(figsize=(12.4,5)).add_subplot(1,1,1)
	else:
		ax = plt.figure(figsize=(24.8,10)).add_subplot(1,1,1)

	plt.gcf().canvas.set_window_title('Elenco Voti')
	plt.grid(which='both')
	major_ticks = np.arange(0, 11, 1)
	minor_ticks = np.arange(0, 11, 0.5)
	ax.set_xticks(major_ticks)
	ax.set_xticks(minor_ticks, minor=True)
	ax.set_yticks(major_ticks)
	ax.set_yticks(minor_ticks, minor=True)
	ax.grid(which='major', alpha=0.5)
	ax.grid(which='minor', alpha=0.2)
	plt.axhline(y=6, alpha = 0.2, color='r', linestyle='-', label = 'Sufficienza')
	
	for subj in marks_dict:
		avg1 = 0
		plt.plot(list(reversed(marks_dict[subj])), label = subj, marker = 'o')
		print(subj + ': ' + str(' - '.join(str(x) for x in reversed(marks_dict[subj]))))
		max1.append(len(marks_dict[subj]))

		for v in marks_dict[subj]:
			avg += v
		
		for v in marks_dict[subj]:
			avg1 += v

		tot += len(marks_dict[subj])
		print('Media: ' + str(round(avg1 / len(marks_dict[subj]), 2)), end = '\n\n')

	avg /= tot
	print('\nLa media dei voti e\': ' + str(round(avg, 2)))
	plt.axis([-0.1, max(max1), 0, 10.1])
	plt.axhline(y = avg, alpha = 0.2, color='g', linestyle='-', label = 'Media')
	
	if args.file:
		plt.legend(loc = 4)
		plt.subplots_adjust(left = 0.02, right = 0.98, top = 0.98, bottom = 0.05)
		plt.savefig(args.file + '.png' if not args.file.endswith('.png') else args.file, format = 'png', dpi = 300)
		print('\nFile has been saved on ' + args.file + ('.png' if not args.file.endswith('.png') else ''))
	else:
		plt.legend(bbox_to_anchor=(1, 1), loc="upper left", prop={'size': 8})
		plt.subplots_adjust(left=0.02, right=0.7, top=0.98, bottom=0.05)
		plt.show()

def get_marks():
	base_header={'x-cod-min': SCHOOL_CODE, 'x-key-app': ARGOAPI_KEY, 'x-version': ARGOAPI_VERSION, 'user-agent': USER_AGENT}
	loginheader={'x-user-id': USERNAME, 'x-pwd': PASSWORD}
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
		raise ConnectionRefusedError('Connection error [ERROR: ' + str(r.status_code) + ']')

	return r.text

parser = argparse.ArgumentParser()
parser.add_argument('-s','--school', required = False)
parser.add_argument('-u','--user', required = False)
parser.add_argument('-p','--password', required = False)
parser.add_argument('-f','--file', required = False)
args = parser.parse_args()

SCHOOL_CODE = input('School Code: ') if not args.school else args.school
USERNAME = input('Username: ') if not args.user else args.user
PASSWORD = getpass.getpass('Password: ') if not args.password else args.password
ARGOAPI_URL = 'https://www.portaleargo.it/famiglia/api/rest/'
ARGOAPI_KEY = 'ax6542sdru3217t4eesd9'
ARGOAPI_VERSION = '2.0.2'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

print()
get_graph()
