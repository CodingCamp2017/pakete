package com.itestra.codingcamp.androidpost.utils;

import android.content.Context;
import android.graphics.Typeface;

/**
 * Created by Toni on 24.08.2017.
 */

public class FontawesomeProvider {

    static Typeface font = null;

    public FontawesomeProvider(Context context){
        if(font == null) {
            font = Typeface.createFromAsset(context.getAssets(), "fontawesome-webfont.ttf");
        }
    }

    public Typeface getFontawesome()
    {
        return font;
    }
}
