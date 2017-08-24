package com.itestra.codingcamp.androidpost.exceptions;

/**
 * Created by simon on 24.08.17.
 */

public class InvalidRequestException extends RestException {
    public InvalidRequestException(String message) {
        super(message);
    }
}
