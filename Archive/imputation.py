def to_mean(data_frame, columns):
    data_frame = data_frame.copy()

    def impute_column_to_mean(data_frame, column):
        data_frame[column].fillna(data_frame[column].mean(), inplace = True)

    for column in columns:
        impute_column_to_mean(data_frame, column)

    return data_frame

def using_machine_learning(data_frame, columns):
    import datawig
    return datawig.SimpleImputer.complete(data_frame)