## Логика работы игры

### ДО НАЧАЛА ИГРЫ
Участвующим надо вписать команду, чтобы их добавило в список рандома
Чтобы начать рандом искателей, админу надо будет ввести команду, которая рандомно выберет 1 человека и перенесёт в команду искателей
Для того чтобы перенести остальных людей в команду хайдеров, админу надо вписать команду, (TODO) которая перенесёт хайдеров в коробку с вещами из ресурспака
Для того чтобы начать игру, админу надо вписать команду, после которой команда хайдеров тепнется в начало для хайдеров, а команда искателей тепнется в начало искателей


### ДЛЯ ИСКАТЕЛЕЙ
* Если искатель ударит хайдера 3 раза, то хайдер заморозится
* Если искатель ударит искателя, то нечего не произойдёт
* Искатель не может размораживать хайдеров

### ДЛЯ ХАЙДЕРОВ
* Если хайдер ударит замёрзшего хайдера, то замёрзший хайдер разморозиться
* Один хайдер может размораживать только 1 хайдера
* Хайдер должен стоять на месте во время разморозки чтобы таймер разморозки не сбрасывался
* Если хайдера разморозили, то у него сбросится счётчик ударов, TODO: но у него счётчик ударов уменьшится до 2х
* TODO: Если хайдера разморозили второй раз, то у него сбросится счётчик ударов, и у счётчик ударов уменьшиться до 1го
* TODO: Если хайдера заморозили 3ий раз, то он переходит в команду искателей
* Если замёрзший хайдер ударит замёрзшего хайдера, то нечего не произойдёт
* Если хайдер ударит хайдера, то нечего не произойдёт
* Если хайдер ударит искателя, то нечего не произойдёт
* TODO: Хайдер замёрзшего хадера размораживает 3 секунды
* Если замёрзший хайдер не был разморожен 40 секунд, то он переходит в команду искателей

### ТАЙМЕРЫ
* Таймер до конца игры
  Таймер один для всех
  Время для него можно изменять до начала игры
  Начало отсчёта будет в начале игры
  Игра заканчивается, когда таймер срабатывает, проверка условия победы
  Условие победы: если в команде хайдеров люди есть, то победа хайдеров, если нету то победа искателей
  Отсчёт закончить если в команде хайдеров больше нету людей
* Таймер до конца заморозки
  Таймер для каждого хайдера свой
  Время для него 40 секунды
  Начало отсчёта будет в начале заморозки хайдера
  Если замёрзший хайдер не был разморожен до срабатывания таймера, то он переходит в команду искателей
* Таймер разморозки хайдера
  Таймер для каждого незамёрзшего хайдера свой
  Время для него 3 секунды
  Начало отсчёта будет в начало разморозки
  Конец будет после окончания таймера
  Хайдер должен непрерывно взаимодействовать с замерзшим, иначе таймер сбрасывается
* Таймер до выхода искателей
  Таймер один для всех
  Время для него 1 минута
  Начало отсчёта будет в начале игры
  После окончания таймера, искатели тепаются в начало хайдеров

