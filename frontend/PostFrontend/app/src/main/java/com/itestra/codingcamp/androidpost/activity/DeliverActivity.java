package com.itestra.codingcamp.androidpost.activity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentResult;
import com.itestra.codingcamp.androidpost.R;

/**
 * Created by Toni on 23.08.2017.
 */

public class DeliverActivity extends BaseActivity{
    @Override
    int getContentViewId() {
        return R.layout.activity_deliver;
    }

    @Override
    int getNavigationMenuItemId() {
        return R.id.navigation_deliver;
    }

    @Override
    void sendData() {
        restInterface.deliverPacket(((EditText)findViewById(R.id.edittext_packet_id)).getText().toString());
        ((EditText)findViewById(R.id.edittext_packet_id)).setText("");
        packet_id = "";
        Toast.makeText(this, "Packet delivered!", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Button scanButton = (Button) findViewById(R.id.button_scan);
        scanButton.setOnClickListener(v -> {
            if (ActivityCompat.checkSelfPermission(DeliverActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                startScan();
            } else {
                String permission = Manifest.permission.CAMERA;
                if (ContextCompat.checkSelfPermission(DeliverActivity.this, permission) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(DeliverActivity.this, new String[]{permission}, PERMISSION_REQUEST_CODE);
                }
            }
        });

        ((EditText)findViewById(R.id.edittext_packet_id)).setText(packet_id);
    }
}
