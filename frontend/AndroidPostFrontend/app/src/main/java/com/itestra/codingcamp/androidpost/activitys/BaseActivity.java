package com.itestra.codingcamp.androidpost.activitys;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;
import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.NoScanButtonException;
import com.itestra.codingcamp.androidpost.rest.RestInterface;
import com.itestra.codingcamp.androidpost.utils.FakeDataProvider;
import com.itestra.codingcamp.androidpost.utils.FontawesomeProvider;

public abstract class BaseActivity extends AppCompatActivity implements BottomNavigationView.OnNavigationItemSelectedListener {

    protected static int PERMISSION_REQUEST_CODE = 1;
    protected static FakeDataProvider fakeDataProvider;
    protected static FontawesomeProvider fontawesomeProvider;
    protected static String packet_id;
    protected RestInterface restInterface;
    protected BottomNavigationView navigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(getContentViewId());

        fakeDataProvider = new FakeDataProvider(this.getApplicationContext());
        fontawesomeProvider = new FontawesomeProvider(this.getApplicationContext());

        navigationView = (BottomNavigationView) findViewById(R.id.navigation);
        navigationView.setOnNavigationItemSelectedListener(this);

        restInterface = new RestInterface();

        findViewById(R.id.floating_action_button_send).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendData();
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        switch (requestCode) {
            case 1:
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    startScan();
                }
                break;
        }
    }

    protected void startScan() {
        IntentIntegrator integrator = new IntentIntegrator(this);
        integrator.initiateScan();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        if (scanResult != null) {
            if(scanResult.getContents() != null) {
                handleScanResult(scanResult);
                Toast.makeText(this, scanResult.getContents(), Toast.LENGTH_LONG).show();
            }
        }
    }

    private void handleScanResult(IntentResult scanResult) {
        EditText editTextId = (EditText) findViewById(R.id.edittext_packet_id);
        editTextId.setText(scanResult.getContents());
    }

    @Override
    protected void onStart() {
        super.onStart();
        updateNavigationBarState();
    }

    // Remove inter-activity transition to avoid screen tossing on tapping bottom navigation items
    @Override
    public void onPause() {
        super.onPause();
        overridePendingTransition(0, 0);
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        navigationView.post(() -> {
            int itemId = item.getItemId();
            if (itemId == R.id.navigation_add) {
                startActivity(new Intent(this, AddActivity.class));
            } else if (itemId == R.id.navigation_relocate) {
                startActivity(new Intent(this, RelocateActivity.class));
            } else if (itemId == R.id.navigation_deliver) {
                startActivity(new Intent(this, DeliverActivity.class));
            }
            finish();
        });
        return true;
    }

    private void updateNavigationBarState() {
        int actionId = getNavigationMenuItemId();
        selectBottomNavigationBarItem(actionId);
    }

    void selectBottomNavigationBarItem(int itemId) {
        Menu menu = navigationView.getMenu();
        for (int i = 0, size = menu.size(); i < size; i++) {
            MenuItem item = menu.getItem(i);
            boolean shouldBeChecked = item.getItemId() == itemId;
            if (shouldBeChecked) {
                item.setChecked(true);
                break;
            }
        }
    }

    public void initScanButton() throws NoScanButtonException {
        Button scanButton = (Button) findViewById(R.id.button_scan);
        if (scanButton == null) {
            throw new NoScanButtonException();
        }
        scanButton.setTypeface(fontawesomeProvider.getFontawesome());
        scanButton.setOnClickListener(v -> {
            if (ActivityCompat.checkSelfPermission(BaseActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                startScan();
            } else {
                String permission = Manifest.permission.CAMERA;
                if (ContextCompat.checkSelfPermission(BaseActivity.this, permission) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(BaseActivity.this, new String[]{permission}, PERMISSION_REQUEST_CODE);
                }
            }
        });
    }

    abstract int getContentViewId();

    abstract int getNavigationMenuItemId();

    abstract void sendData();
}