import json

# Your list of pairs
data = [
    [('Потпредседник др. ', {}), ('Светислав Поповић : ', {'bold': True}), ('0што се за реч није нико пријавио, а листа. говор“ ника. је исцрпљена, проглашујем претрес завршепим па прелазимо на гласање. Госп. известиоца молим, да прочита. члан 22. (Гласови: Не треба га читати, већ је прочитан.) Дакле прелазимо на гласање. Она, господа, која примају члан 22. по предлогу одборовом нека изволе седети, а господа, која су против. тога. предлога нека изволе дићи руке. (Ђећина. седи.) Предлог је примљен.', {})],
    [('НАРОДНЕ СКУПШТИНЕ ', {'bold': True}), ('КРАЉЕВИНЕ СРБА, ХРВАТА И СЛОВЕНАЦА', {})],
    [('Председавао · Потпредседник др. ', {}), ('Светислав Поповић.', {'bold': True}), ('', {})],
    [('Присутни су господа: Министар Финансија, лр. ', {}), ('Коста Кумануди: ', {'bold': True}), ('Министар. Пољопривреде и Вода, ', {}), ('Иван Пу', {'bold': True}), ("цељ и Министар 'Трговине и Индустрије др. Мехмед Спахо.        ј", {})],
    [(', Потпредседник. др. ', {}), ('Светислав Поповић: ', {'bold': True}), ('Отварам 11. одбореку седницу. Молим господина. заменика секретара, да изволи прочитати записник 10. седнице Законодавног Одбора.', {})],
    [('Заменик секретара, административни чиновник. Народне Скупштине ', {}), ('Света Михајловић ', {'bold': True}), ('чита записник. 10. седнице Законодавног Одбора.', {})]
]

# Save the data to a JSON file
with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False)


# with open('output.json') as f:
    # d = json.load(f)
    
    
    # print(d)
