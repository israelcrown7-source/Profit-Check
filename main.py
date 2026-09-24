from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


def business_report(product, selling_price, cost_price, quantity):
    revenue = selling_price * quantity
    total_cost = cost_price * quantity
    profit = revenue - total_cost
    profit_per_item = profit / quantity if quantity else 0

    lines = []
    lines.append(f"***** BUSINESS REPORT FOR {product.upper()} *****")
    lines.append(f"Revenue: NGN{revenue:,.2f}")
    lines.append(f"Total Cost: NGN{total_cost:,.2f}")
    lines.append(f"Profit on {product}: NGN{profit:,.2f}")
    lines.append(f"Profit Per Item: NGN{profit_per_item:,.2f}")

    if profit > 0:
        lines.append("Status: Profit 👍")
    elif profit == 0:
        lines.append("Status: Break-Even")
    else:
        lines.append("Status: Loss 👎")

    return "\n".join(lines)


class FarmCalculatorApp(App):
    def build(self):
        self.title = "ProfitCheck"
        root = BoxLayout(orientation="vertical", padding=20, spacing=10)

        form = GridLayout(cols=2, spacing=10, size_hint_y=None, height=220)

        form.add_widget(Label(text="Item Name:"))
        self.product_input = TextInput(multiline=False)
        form.add_widget(self.product_input)

        form.add_widget(Label(text="Selling Price (NGN):"))
        self.selling_price_input = TextInput(multiline=False, input_filter="float")
        form.add_widget(self.selling_price_input)

        form.add_widget(Label(text="Cost Price (NGN):"))
        self.cost_price_input = TextInput(multiline=False, input_filter="float")
        form.add_widget(self.cost_price_input)

        form.add_widget(Label(text="Quantity:"))
        self.quantity_input = TextInput(multiline=False, input_filter="float")
        form.add_widget(self.quantity_input)

        root.add_widget(form)

        calc_button = Button(text="Calculate Report", size_hint_y=None, height=60)
        calc_button.bind(on_press=self.calculate)
        root.add_widget(calc_button)

        scroll = ScrollView()
        self.result_label = Label(
            text="Your report will appear here.",
            size_hint_y=None,
            halign="left",
            valign="top",
        )
        self.result_label.bind(
            width=lambda *x: self.result_label.setter("text_size")(
                self.result_label, (self.result_label.width, None)
            ),
            texture_size=lambda *x: self.result_label.setter("height")(
                self.result_label, self.result_label.texture_size[1]
            ),
        )
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)

        return root

    def calculate(self, instance):
        product = self.product_input.text.strip() or "Product"
        try:
            selling_price = float(self.selling_price_input.text or 0)
            cost_price = float(self.cost_price_input.text or 0)
            quantity = float(self.quantity_input.text or 0)
        except ValueError:
            self.result_label.text = "Please enter valid numbers."
            return

        if quantity == 0:
            self.result_label.text = "Quantity cannot be zero."
            return

        report = business_report(product, selling_price, cost_price, quantity)
        self.result_label.text = report


if __name__ == "__main__":
    FarmCalculatorApp().run()
