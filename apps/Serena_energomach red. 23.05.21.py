# Посмотрим на данные с помощью библиотеки sweeetviz
pip install sweetviz

import sweetviz as sv

import pandas as pd

av_pr_sac_2020 = pd.read_excel('Аварии_Причины_САЦ_2020.xlsx')

av_pr_sac_2020_report = sv.analyze(av_pr_sac_2020)
av_pr_sac_2020_report.show_html('av_pr_sac_2020_report.html')

av_pog_sac_2020 = pd.read_excel('Аварии_погода_САЦ_2020.xlsx')

av_pog_sac_2020['Субъект РФ'] = av_pog_sac_2020['Субъект РФ'].astype(str)

av_pog_sac_2020_report = sv.analyze(av_pog_sac_2020)
av_pog_sac_2020_report.show_html('av_pog_sac_2020_report.html')

av_pog_sac = pd.read_excel('Аварии_погода_САЦ.xlsx')

av_pog_sac_report = sv.analyze(av_pog_sac)
av_pog_sac_report.show_html('av_pog_sac_report.html')

# В результате работать будем только с файлом "Аварии_Причины_САЦ_2020", как наиболее полным

# Переименуем столбцы
av_pr_sac_2020 = av_pr_sac_2020.rename(columns={"Дата (местное время)": "date", "Субъект РФ2": "region", "Причина": "cause"})

# Удалим отключения, вызванные животными и птицами
indexNames = av_pr_sac_2020[av_pr_sac_2020['cause'] == 'Воздействие животных и птиц'].index
av_pr_sac_2020 = av_pr_sac_2020.drop(indexNames)

# Как видим, число отключений сократилось с 7389 до 5124

# Считаем загруженные с rp5.ru сведения о погоде в 2020 году по регионам РФ
pog_rf_2020 = pd.read_excel('arhiv.xlsx')

# Приведем в файлах отключений и погоды столбец даты к формату datetime и выделим в отдельные столбцы порядковый день года и час (отключения/замера погоды)
pog_rf_2020.loc[:,'date'] = pd.to_datetime(pog_rf_2020['date'])
pog_rf_2020['День года'] = pog_rf_2020['date'].dt.dayofyear
pog_rf_2020['Час'] = pog_rf_2020['date'].dt.hour

av_pr_sac_2020.loc[:,'date'] = pd.to_datetime(av_pr_sac_2020['date'])
av_pr_sac_2020['День года'] = av_pr_sac_2020['date'].dt.dayofyear
av_pr_sac_2020['Час отключения'] = av_pr_sac_2020['date'].dt.hour

# Приведем часы к ближайшим замерным по погоде (данные с rp5.ru выгружаются кратно 3 часам)
def myround(x, base=3):
    return base * round(x/base)
av_pr_sac_2020['Час отключения'] = myround(av_pr_sac_2020['Час отключения'])

# Приведем к тому же формату час замера в файле погоды и посмотрим на файл погоды
pog_rf_2020['Час'] = myround(pog_rf_2020['Час'])

# В качестве идентификатора для сопоставления данных в файлах отключений и погоды создадим столбец ident, в котором находится название региона, порядковый номер дня в 2020 году и номер часа
av_pr_sac_2020['ident'] = av_pr_sac_2020['region'].astype(str) + ',' + av_pr_sac_2020['День года'].astype(str) + ',' + av_pr_sac_2020['Час отключения'].astype(str)

# Аналогично поступим с файлом погоды - создадим столбец ident для сопоставления данных с файлом отключений
pog_rf_2020['ident'] = pog_rf_2020['region'].astype(str) + ',' + pog_rf_2020['День года'].astype(str) + ',' + pog_rf_2020['Час'].astype(str)

# Создаем столбец if_acc, в который запишем True, если в этот момент в этом регионе не было отключения, и False, если было
pog_rf_2020['if_acc'] = pog_rf_2020['ident'][~pog_rf_2020['ident'].isin(av_pr_sac_2020['ident'])]
pog_rf_2020['if_acc'] = pog_rf_2020['if_acc'].notna()

# Как видим, в подавляющем большинстве временных срезов в большинстве регионов не было отключений, что логично
pog_rf_2020['if_acc'].describe()

# Сведем все многообразие данных по погоде к типовым значениям (все виды дождей - "дождь" и т.д.)
WW_dict = {'Морось незамерзающая непрерывная слабая в срок наблюдения. ' : 'Морось', 'Морось незамерзающая с перерывами слабая в срок наблюдения. ' : 'Морось',
      'Морось незамерзающая непрерывная умеренная в срок наблюдения. ' : 'Морось', 'Морось (незамерзающая) или снежные зерна неливневые. ' : 'Морось',
      'Дымка. ' : 'Дымка', ' ' : 'Без осадков', 'Снег непрерывный умеренный в срок наблюдения. ' : 'Снег', 'Снег неливневый. ' : 'Снег', '  Диаметр отложения мокрого снега составляет 1 мм.' : 'Снег',
      '  Диаметр отложения мокрого снега составляет 2 мм.': 'Снег', 'Снег неливневый.  Диаметр отложения мокрого снега составляет 2 мм.' : 'Снег',
      'Дождь (незамерзающий) неливневый. ' : 'Дождь', 'Снег непрерывный слабый в срок наблюдения. ' : 'Снег', 'Замерзающая морось или замерзающий дождь неливневые. ' : 'Снег',
      'Ливневый снег слабый в срок наблюдения или за последний час. ' : 'Снег', 'Ливневый снег умеренный или сильный в срок наблюдения или за последний час.  Диаметр отложения при гололеде составляет 1 мм.' : 'Снег',
      'Снежные зерна (с туманом или без него). ' : 'Снег', 'Дождь незамерзающий непрерывный слабый в срок наблюдения. ' : 'Дождь', 'Снег с перерывами слабый в срок наблюдения. ' : 'Снег',
      'Дождь незамерзающий с перерывами слабый в срок наблюдения. ' : 'Дождь', 'Ливневый снег умеренный или сильный в срок наблюдения или за последний час. ' : 'Снег',
      'Облака в целом образовывались или развивались. ' : 'Без осадков', 'Облака в целом рассеиваются или становятся менее развитыми. ' : 'Без осадков',
      'Ливневый(ые) дождь(и) со снегом слабый(ые) в срок наблюдения или за последний час. ' : 'Дождь', 'Ливневый(ые) дождь(и) со снегом умеренный(ые) или сильный(ые) в срок наблюдения или за последний час. ' : 'Дождь',
      'Ливневый(ые) дождь(и) слабый(ые) в срок наблюдения или за последний час. ' : 'Дождь', 'Дождь или морось со снегом умеренные или сильные. ' : 'Дождь', 
      'Морось и дождь умеренные или сильные. ' : 'Дождь', 'Туман или ледяной туман, неба не видно, без заметного изменения интенсивности в течение последнего часа. ' : 'Туман', 
      'Ливневый(ые) дождь(и). ' : 'Дождь', 'Дождь незамерзающий непрерывный умеренный в срок наблюдения. ' : 'Дождь', 
      'Ливневый(ые) дождь(и) умеренный(ые) или сильный(ые) в срок наблюдения или за последний час. ' : 'Дождь', 'Дождь незамерзающий непрерывный сильный в срок наблюдения. ' : 'Дождь',
      'Дождь незамерзающий с перерывами сильный в срок наблюдения. ' : 'Дождь', 'Гроза слабая или умеренная без града, но с дождем и/или снегом в срок наблюдения. ' : 'Гроза',
      'Гроза, но без осадков, в срок наблюдения. ' : 'Гроза', 'Умеренный или сильный дождь в срок наблюдения. Гроза в течение последнего часа, но не в срок наблюдения. ' : 'Дождь',
      'Туман или ледяной туман, неба не видно, начался или усилился в течение последнего часа. ' : 'Туман', 'Ливневая снежная крупа или небольшой град с дождем или без него, или дождь со снегом слабые в срок наблюдения или за последний час. ' : 'Град',
      'Ливневый град, или дождь и град. ' : 'Град', 'Дождь незамерзающий с перерывами умеренный в срок наблюдения. ' : 'Дождь', 'Ливневый снег или ливневый дождь и снег. ' : 'Снег',
      'Дождь или морось со снегом слабые. ' : 'Дождь', 'Дождь со снегом или ледяная крупа неливневые. ' : 'Снег', 'Снег непрерывный сильный в срок наблюдения. ' : 'Снег',
      'Снег с перерывами сильный в срок наблюдения. ' : 'Снег'}
pog_rf_2020.loc[:,'common'] = pog_rf_2020.loc[:,'common'].map(WW_dict)

# Замением пропущенное описание погоды в графе "common" на "без осадков", так как пропуски обычно соответствуют обычной погоде
pog_rf_2020['temp'].fillna(pog_rf_2020['temp'].mean(), inplace = True)
pog_rf_2020['wind_speed'].fillna(pog_rf_2020['wind_speed'].mean(), inplace = True)
pog_rf_2020['common'].fillna(value={'common': 'Без осадков'}, inplace = True)

# Начинаем строить предиктивную модель. X - предикторы, y - предсказываемая независимая переменная (есть отключение/нет отключения)
X = pog_rf_2020[['temp','wind_speed','common']]
y = pog_rf_2020.if_acc

# Применим one-hot encoding для категориальной зависимой переменной (common - общее описание погоды)
X = pd.get_dummies(X)

# Поскольку имеет место большая несбалансированность классов, используем undersampling - сократим число объектов мажоритарного класса
pip install imblearn
from imblearn.under_sampling import RandomUnderSampler
rus = RandomUnderSampler(sampling_strategy=0.3)
X_rus, y_rus = rus.fit_resample(X, y)

# Разобъем все множество на train/test в соотношении 3 к 1 (установленное по дефолту)
import sklearn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_rus, y_rus)

# Обучим модель градиентного бустинга. При этом найдем его оптимальные гиперпараметры поиском по сетке GridSearch с кросс-валидацией на 5 фолдов
from sklearn.ensemble import GradientBoostingClassifier
clf_gb = GradientBoostingClassifier()
parameters_gb = {'n_estimators':range(1,8), 'max_depth':range(1,8), 'min_samples_split':range(2,8)}
search_gb = GridSearchCV(clf_gb, parameters_gb, cv = 5)
search_gb.fit(X_train, y_train)
best_gb = search_gb.best_estimator_
print('Параметры лучшего градиентного бустинга', search_gb.best_params_)
print('Точность лучшего градиентного бустинга на train set:', best_gb.score(X_train, y_train))
print('Точность лучшего градиентного бустинга на test set:', best_gb.score(X_test, y_test))

# Теперь с помощью обученной на исторических данных модели градиентного бустинга предскажем вероятности отключений на 24 и 25 мая в регионах РФ
progn_24_05 = pd.read_excel('Прогноз_24_05_2021.xlsx')
progn_25_05 = pd.read_excel('Прогноз_25_05_2021.xlsx')

progn_24_05.loc[:,'common'] = progn_24_05.loc[:,'common'].map(WW_dict)
progn_25_05.loc[:,'common'] = progn_25_05.loc[:,'common'].map(WW_dict)
X_pred_24_05 = progn_24_05[['temp','wind_speed','common']]
X_pred_24_05 = pd.get_dummies(X_pred_24_05)
X_pred_25_05 = progn_25_05[['temp','wind_speed','common']]
X_pred_25_05 = pd.get_dummies(X_pred_25_05)
X_pred_24_05['temp'].fillna(X_pred_24_05['temp'].mean(), inplace = True)
X_pred_24_05['wind_speed'].fillna(X_pred_24_05['wind_speed'].mean(), inplace = True)
X_pred_25_05['temp'].fillna(X_pred_24_05['temp'].mean(), inplace = True)
X_pred_25_05['wind_speed'].fillna(X_pred_24_05['wind_speed'].mean(), inplace = True)

predict_24_05 = best_gb.predict_proba(X_pred_24_05)
predict_25_05 = best_gb.predict_proba(X_pred_25_05)
predict_24_05 = pd.DataFrame(data=predict_24_05)
predict_24_05 = predict_24_05.drop([1], axis=1)
predict_25_05 = pd.DataFrame(data=predict_25_05)
predict_25_05 = predict_25_05.drop([1], axis=1)

progn_24_05_with_predict = progn_24_05.join(predict_24_05)
progn_25_05_with_predict = progn_25_05.join(predict_25_05)
progn_24_05_with_predict = progn_24_05_with_predict.rename(columns={0: "probability"})
progn_25_05_with_predict = progn_25_05_with_predict.rename(columns={0: "probability"})

# Таким образом, получаем прогноз вероятности отключения по субъектам РФ на завтра и послезавтра - передаем во front-end
progn_24_05_with_predict.to_excel("output1.xlsx")
progn_25_05_with_predict.to_excel("output2.xlsx")