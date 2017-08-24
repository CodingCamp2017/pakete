package com.itestra.codingcamp.androidpost.exceptions;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by simon on 24.08.17.
 */

public class ServerException extends RestException {
    public ServerException(String error) {
        super(error);
    }
}