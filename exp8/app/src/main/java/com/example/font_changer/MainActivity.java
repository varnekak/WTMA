package com.example.font_changer;

import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.res.ResourcesCompat;

public class MainActivity extends AppCompatActivity {

    TextView sampleText;
    Button changeStyleButton;
    boolean isChanged = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sampleText = findViewById(R.id.sampleText);
        changeStyleButton = findViewById(R.id.changeStyleButton);

        changeStyleButton.setOnClickListener(v -> {

            if (!isChanged) {
                // Change color
                sampleText.setTextColor(Color.parseColor("#FF5722"));

                // Change font + style
                Typeface typeface = ResourcesCompat.getFont(this, R.font.roboto_regular);
               sampleText.setTypeface(typeface, Typeface.BOLD_ITALIC);

                Toast.makeText(this, "Style Changed!", Toast.LENGTH_SHORT).show();

            } else {
                // Reset
                sampleText.setTextColor(Color.BLACK);
                sampleText.setTypeface(Typeface.DEFAULT);

                Toast.makeText(this, "Style Reset!", Toast.LENGTH_SHORT).show();
            }

            isChanged = !isChanged;
        });
    }
}