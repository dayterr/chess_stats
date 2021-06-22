from http import HTTPStatus

from bs4 import BeautifulSoup
import requests
import termcolor


def start():
    username = input('Please, enter a username: ')

    url = f'https://lichess.org/@/{username}/all'
    req = requests.get(url)
    if req.status_code == HTTPStatus.NOT_FOUND:
        print('Invalid username!')
        start()
    else:
        get_stats(req.content)


def get_stats(page):
    soup = BeautifulSoup(page, 'html.parser')
    total = soup.find('a', attrs={'class': 'to-all'})
    total = int(total.text.replace(',', '').strip('games'))
    won = soup.find('a', attrs={'class': 'to-win'})
    won = int(won.text.replace(',', '').strip('wins'))
    lost = soup.find('a', attrs={'class': 'to-loss'})
    lost = int(lost.text.replace(',', '').strip('losses'))
    draw = soup.find('a', attrs={'class': 'to-draw'})
    draw = int(draw.text.replace(',', '').strip('draws'))
    won_pct = int(round(won/total, 2) * 100)
    lost_pct = int(round(lost/total, 2) * 100)
    draw_pct = int(round(draw/total, 2) * 100)

    wins = f'Won: {won_pct}% of games ({won} games)'
    draws = f'Draws: {draw_pct}% of games ({draw} games)'
    los = f'Lost: {lost_pct}% of games ({lost} games)'
    tots = f'Total: {total}'
    spent = soup.find_all('p')[-1].text

    termcolor.cprint(spent, color='cyan')
    termcolor.cprint(wins, color='green')
    termcolor.cprint(draws, color='yellow')
    termcolor.cprint(los, color='red')
    termcolor.cprint(tots, color='cyan')


if __name__ == '__main__':
    start()
