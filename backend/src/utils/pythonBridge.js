const { spawn } = require('child_process');
const path = require('path');

const bridgePath = path.resolve(__dirname, '../../python_bridge/api_bridge.py');

/**
 * Calls the Python blockchain bridge.
 * @param {string} action The action to perform (e.g., 'get_chain', 'get_stats')
 * @param {Object} data Any payload needed for the action
 * @returns {Promise<Object>} The JSON response from Python
 */
const callBlockchain = (action, data = {}) => {
  return new Promise((resolve, reject) => {
    // Determine the python command based on OS, often 'python' on windows and 'python3' on unix
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    
    const child = spawn(pythonCmd, [
      bridgePath,
      action,
      '--data',
      JSON.stringify(data)
    ]);

    let stdoutData = '';
    let stderrData = '';

    child.stdout.on('data', (chunk) => {
      stdoutData += chunk.toString();
    });

    child.stderr.on('data', (chunk) => {
      stderrData += chunk.toString();
    });

    child.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}. Stderr: ${stderrData}`);
        return reject(new Error(`Blockchain error: ${stderrData || 'Unknown error'}`));
      }
      
      try {
        const result = JSON.parse(stdoutData);
        if (result.error) {
          reject(new Error(result.error));
        } else {
          resolve(result);
        }
      } catch (err) {
        console.error("Failed to parse JSON from Python:", stdoutData);
        reject(new Error("Invalid response from blockchain bridge"));
      }
    });
  });
};

module.exports = { callBlockchain };
