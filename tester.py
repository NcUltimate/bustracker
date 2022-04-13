import alexa

test_event = {
  "session": {
    "new": True,
    "sessionId": "SessionId.59528309-23c8-40aa-ac9d-addb27149700",
    "application": {
      "applicationId": "amzn1.ask.skill.0f2db0c9-f3ab-4720-91b1-a22cd6957588"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AFM4FVZRMWEDVSY3MJJWJWDQM3GGBPDXBXU3BJOAL52FJEASAOQ43UBCPIFQERQVMDHFHRTLLCPSH4CEAZ37WUBTXJA4VLHVANNHN7Z3EV7ESXGBLZX27CSG6FGU3UT5IXZP3EIUSMP5NR3SIOEEE2UOUF25NTNLX5VLDPLNUCL4VFDR6NOAJQWP4ZGCNTYSKZ6SODZHUVTABCQ"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.49f4d5da-94eb-4dfd-8fae-b945aacbb9b9",
    "intent": {
      "name": "BusIntent",
      "slots": {
        "AdverbClause": {
          "name": "AdverbClause",
          "value": "what's"
        },
        "BusStop": {
          "name": "BusStop",
          "value": "roosevelt and michigan"
        },
        "BusDirection": {
          "name": "BusDirection"
        },
        "Route": {
          "name": "Route",
          "value": "151"
        }
      }
    },
    "locale": "en-US",
    "timestamp": "2017-08-13T21:26:36Z"
  },
  "context": {
    "AudioPlayer": {
      "playerActivity": "IDLE"
    },
    "System": {
      "application": {
        "applicationId": "amzn1.ask.skill.0f2db0c9-f3ab-4720-91b1-a22cd6957588"
      },
      "user": {
        "userId": "amzn1.ask.account.AFM4FVZRMWEDVSY3MJJWJWDQM3GGBPDXBXU3BJOAL52FJEASAOQ43UBCPIFQERQVMDHFHRTLLCPSH4CEAZ37WUBTXJA4VLHVANNHN7Z3EV7ESXGBLZX27CSG6FGU3UT5IXZP3EIUSMP5NR3SIOEEE2UOUF25NTNLX5VLDPLNUCL4VFDR6NOAJQWP4ZGCNTYSKZ6SODZHUVTABCQ"
      },
      "device": {
        "supportedInterfaces": {}
      }
    }
  },
  "version": "1.0"
}

print alexa.lambda_handler(test_event, {})

