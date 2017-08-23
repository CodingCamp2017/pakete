package com.itestra.codingcamp.androidpost.activity;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.widget.ViewSwitcher;

import com.itestra.codingcamp.androidpost.R;

import view.AddView;
import view.DeliverView;
import view.RelocateView;

public class StartActivity extends AppCompatActivity {

    private ViewGroup contentViewGroup;

    private AddView addView;
    private RelocateView relocateView;
    private DeliverView deliverView;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_add:
                    contentViewGroup.removeAllViews();
                    contentViewGroup.addView(addView);
                    return true;
                case R.id.navigation_relocate:
                    contentViewGroup.removeAllViews();
                    contentViewGroup.addView(relocateView);
                    return true;
                case R.id.navigation_deliver:
                    contentViewGroup.removeAllViews();
                    contentViewGroup.addView(deliverView);
                    return true;
            }
            return false;
        }

    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);

        contentViewGroup = (ViewGroup) findViewById(R.id.contentViewGroup);
        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        initViews();
    }

    private void initViews() {
        addView = new AddView(this);
        relocateView = new RelocateView(this);
        deliverView = new DeliverView(this);
    }

}
