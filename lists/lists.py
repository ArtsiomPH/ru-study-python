class ListExercise:
    @staticmethod
    def replace(input_list: list[int]) -> list[int]:
        """
        Заменить все положительные элементы целочисленного списка на максимальное значение
        элементов списка.

        :param input_list: Исходный список
        :return: Список с замененными элементами
        """
        max_item = 0

        for item in input_list:
            if item > max_item:
                max_item = item

        for index, item in enumerate(input_list):
            if item > 0:
                input_list[index] = max_item
        return input_list

    @staticmethod
    def search(input_list: list[int], query: int) -> int:
        """
        Реализовать двоичный поиск
        Функция должна возвращать индекс элемента

        :param input_list: Исходный список
        :param query: Искомый элемент
        :return: Номер элемента
        """

        def binary_search(search_list: list[int], element: int, start: int, finish: int) -> int:
            if start > finish:
                return -1

            mid = (start + finish) // 2

            if query == input_list[mid]:
                return mid
            elif query > input_list[mid]:
                return binary_search(search_list, element, mid + 1, finish)
            else:
                return binary_search(search_list, element, start, mid - 1)

        begin = 0
        end = len(input_list) - 1

        index = binary_search(input_list, query, begin, end)
        return index
