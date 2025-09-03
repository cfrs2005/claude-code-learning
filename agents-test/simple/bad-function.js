function processData(data, type, options, callback, errorHandler) {
      if (data) {
          if (type === 'json') {
              if (options.validate) {
                  try {
                      var result = JSON.parse(data);
                      if (callback) callback(result);
                  } catch (e) {
                      if (errorHandler) errorHandler(e);
                  }
              }
          }
      }
  }
