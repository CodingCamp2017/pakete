package com.itestra.codingcamp.androidpost.activity;

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
    void handleScanResult(IntentResult scanResult) {

    }
}
