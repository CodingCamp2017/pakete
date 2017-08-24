package com.itestra.codingcamp.androidpost.activity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;

import com.google.zxing.integration.android.IntentResult;
import com.itestra.codingcamp.androidpost.R;

/**
 * Created by Toni on 23.08.2017.
 */

public class RelocateActivity extends BaseActivity{
    @Override
    int getContentViewId() {
        return R.layout.activity_relocate;
    }

    @Override
    int getNavigationMenuItemId() {
        return R.id.navigation_relocate;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        FloatingActionButton floatingActionButton = (FloatingActionButton) findViewById(R.id.floating_action_button_scan);
        floatingActionButton.setOnClickListener(v -> {
            if (ActivityCompat.checkSelfPermission(RelocateActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                startScan();
            } else {
                String permission = Manifest.permission.CAMERA;
                if (ContextCompat.checkSelfPermission(RelocateActivity.this, permission) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(RelocateActivity.this, new String[]{permission}, PERMISSION_REQUEST_CODE);
                }
            }
        });
    }
}
