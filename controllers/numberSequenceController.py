class NumberSequenceController:
    def __init__(self, main_window):
        self.main_window = main_window

        # Setup signals and slots for number sequence-related actions
        self.main_window.generate_numbers_signal.connect(self.generate_numbers)

    def generate_numbers(
        self,
        sequence_name,
        l_bound,
        u_bound,
        label_lbound,
        label_ubound,
        n_groups,
        n_elements,
        order,
        output_window,
    ):
        """
        Generates random numbers based on the input fields and displays them in the output window.
        """
        # get the values from the input fields and convert them to the correct type
        sequence_name = (
            sequence_name.text() if sequence_name.text() != "" else "sequence 1"
        )
        l_bound = int(l_bound.text())
        u_bound = int(u_bound.text())

        n_groups = int(n_groups.text())
        n_elements = int(n_elements.text())

        # check if the values are valid
        if l_bound >= u_bound:
            label_lbound.setStyleSheet("color: red")
            label_ubound.setStyleSheet("color: red")

            return
        else:
            label_lbound.setStyleSheet("color: black")
            label_ubound.setStyleSheet("color: black")

        if n_groups < 1:
            label_dates_n_groups.setStyleSheet("color: red")

            return
        else:
            label_dates_n_groups.setStyleSheet("color: black")

        if n_elements < 1:
            label_dates_n_elements.setStyleSheet("color: red")

            return
        else:
            label_dates_n_elements.setStyleSheet("color: black")

        pcg = PCGRNG(initstate=123)

        numbers = pcg.get_unique_random_sequence(l_bound, u_bound, n_elements)

        if n_groups > 1:
            numbers = sorted(numbers)
            numbers = [numbers[i::n_groups] for i in range(n_groups)]
        else:
            numbers = [numbers]

        if radiobutton_asc.isChecked():
            numbers = [sorted(group) for group in numbers]
        elif radiobutton_desc.isChecked():
            numbers = [sorted(group, reverse=True) for group in numbers]
        else:
            numbers = [group for group in numbers]

        if output_window.isVisible():
            output_window.close()
        else:
            output_window.show()

        # print the numbers
        output_window.output_element.clear()
        output_window.output_element.append(sequence_name)
        output_window.output_element.append("")
        for i, group in enumerate(numbers):
            output_window.output_element.append(f"Group {i+1}:")
            output_window.output_element.append(str(group))
            output_window.output_element.append("")
