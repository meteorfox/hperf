window.HPerf = {

  resourceTimingSupport: function() {
    return (!!window.performance.getEntries);
  },

  performanceTimingSupport: function() {
    return (!!window.performance.timing);
  }

};
