package com.example.animal_care;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.ImageView;

import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class Trace extends AppCompatActivity {
    private static final String IP = "192.168.0.19";
    private static final int PORT = 9999;
    public static final String TAG  = "TCP_CLIENT";

    Button trace = null;
    Button cancel = null;
    MainActivity.TcpThread thread = null;

    static class TcpThread extends Thread{
        private Socket socket;
        private String message = null;
        public void setMessage(String str) { message = str;}
        @Override
        public void run() {
            super.run();
            try {
                socket = new Socket(IP, PORT);                  // 소켓의 생성(socket)과 연결(connect) 동시에 진행하는 코드
                OutputStream os = socket.getOutputStream();            // 자바는 send 없음. 따라서 스트림의 출력을 통해 사용.
                byte[] buf = message.getBytes();                       // 스트림을 통해 SND_BUF 에 쌓이고 네트워크를 통해 빠져나간다.
                os.write(buf);

//                InputStream is = socket.getInputStream();              // 자바는 recv 없음. 따라서 스트림의 입력을 통해 사용.
//                byte[] buf2 = new byte[1024];                          // RCV_BUF 에 쌓이고 스트림을 통해 가져온다.
//                int len = is.read(buf2);
//                String msg = buf2.toString();
//                runOnUiThread(new Runnable() {
//                    @Override
//                    public void run() {
//                        feed.setText(msg);                // 이미지뷰에는 텍스트 지정이 안되기 때문에 주석처리로 삭제
//                    }
//               });
            } catch (Exception e) {
                e.printStackTrace();
            }
            try {
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trace);
        Button main1 = (Button)findViewById(R.id.main1);
        Button movie = (Button)findViewById(R.id.movie);
        Button trace = (Button)findViewById(R.id.trace);
        Button cancel = (Button)findViewById(R.id.cancel);

        main1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        movie.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Trace.this,Movie.class);
                startActivity(intent);
            }
        });
        trace.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String str = toString();
                MainActivity.TcpThread thread3 = new MainActivity.TcpThread();
                thread3.start();
                thread3.setMessage("trace");
                Log.i("thread","thread3");
            }
        });
        cancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String str = toString();
                MainActivity.TcpThread thread4 = new MainActivity.TcpThread();
                thread4.start();
                thread4.setMessage("cancel");
                Log.i("thread","thread4");
            }
        });
    }
}