schema = {
  "v1": {
    "user_updated": {
      "type": "object",
      "properties": {
        "version": {"type": "string"},
        "action": {"type": "string"},
        "data": {
          "type":  "object",
          "properties": {
            "id": {"type":  "number"},
            "is_active": {"type":  "boolean"},
            "role": {"type":  "number"},
            "email": {"type":  "string"}
          }
        }
      }
    },
    "user_created": {
      "type": "object",
      "properties": {
        "version": {"type": "string"},
        "action": {"type": "string"},
        "data": {
          "type":  "object",
          "properties": {
            "id": {"type":  "number"},
            "is_active": {"type":  "boolean"},
            "role": {"type":  "number"},
            "email": {"type":  "string"}
          }
        }
      }
    },
    "user_inactive": {
      "type": "object",
      "properties": {
        "version": {"type": "string"},
        "action": {"type": "string"},
        "data": {
          "type":  "object",
          "properties": {
            "id": {"type":  "number"},
            "is_active": {"type":  "boolean"}
          }
        }
      }
    },
    "task_created": {
      "type": "object",
      "properties": {
        "version": {"type": "string"},
        "action": {"type": "string"},
        "data": {
          "type":  "object",
          "properties": {
            "task_id": {"type":  "number"}
          }
        }
      }
    },
    "task_assigned": {
      "type": "object",
      "properties": {
        "version": {"type": "string"},
        "action": {"type": "string"},
        "data": {
          "type":  "object",
          "properties": {
            "task_id": {"type":  "number"},
            "user_id": {"type":  "number"}
          }
        }
      }
    },
    "task_completed": {
      "type": "object",
      "properties": {
        "version": {"type": "string"},
        "action": {"type": "string"},
        "data": {
          "type":  "object",
          "properties": {
            "task_id": {"type":  "number"},
            "user_id": {"type":  "number"}
          }
        }
      }
    }
  }
}
