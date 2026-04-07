package com.example.calculatorapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.*;

public class MainActivity extends AppCompatActivity {

    EditText e1, e2;
    TextView result;
    Button add, sub, mul, div, clear;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        e1 = findViewById(R.id.editTextNumber1);
        e2 = findViewById(R.id.editTextNumber2);

        add = findViewById(R.id.buttonAdd);
        sub = findViewById(R.id.buttonSubtract);
        mul = findViewById(R.id.buttonMultiply);
        div = findViewById(R.id.buttonDivide);
        clear = findViewById(R.id.buttonClear);

        result = findViewById(R.id.textViewResult);

        add.setOnClickListener(v -> calculate('+'));
        sub.setOnClickListener(v -> calculate('-'));
        mul.setOnClickListener(v -> calculate('*'));
        div.setOnClickListener(v -> calculate('/'));

        clear.setOnClickListener(v -> {
            e1.setText("");
            e2.setText("");
            result.setText("Result will appear here");
        });
    }

    private void calculate(char op) {
        String s1 = e1.getText().toString();
        String s2 = e2.getText().toString();

        if (s1.isEmpty() || s2.isEmpty()) {
            result.setText("Enter both numbers");
            return;
        }

        try {
            double n1 = Double.parseDouble(s1);
            double n2 = Double.parseDouble(s2);
            double res = 0;

            switch (op) {
                case '+': res = n1 + n2; break;
                case '-': res = n1 - n2; break;
                case '*': res = n1 * n2; break;
                case '/':
                    if (n2 == 0) {
                        result.setText("Cannot divide by zero");
                        return;
                    }
                    res = n1 / n2;
                    break;
            }

            result.setText("Result: " + res);

        } catch (Exception e) {
            result.setText("Invalid input");
        }
    }
}