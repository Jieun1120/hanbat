package com.example.animal_care;

import static com.example.animal_care.R.id.movie;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;

public class Movie extends AppCompatActivity {

    private WebView movie;
    private String url = "192.168.0.22:8888";

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_movie);

        movie = (WebView)findViewById(R.id.movie);
        movie.loadUrl(url);
        WebSettings webSettings = movie.getSettings();
        webSettings.setJavaScriptEnabled(true);
        movie.setWebChromeClient(new WebChromeClient());
    }
}