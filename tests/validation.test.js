const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PROTOCOL_FILE = path.join(__dirname, '..', 'rup-protocol-v2.1.yaml');
const VALIDATOR_SCRIPT = path.join(__dirname, '..', 'validate_rup.js');

describe('RUP Validation', () => {
    it('should verify protocol file exists', () => {
        expect(fs.existsSync(PROTOCOL_FILE)).toBe(true);
    });

    it('should verify validator script exists', () => {
        expect(fs.existsSync(VALIDATOR_SCRIPT)).toBe(true);
    });

    it('should validate the protocol file successfully', () => {
        try {
            const output = execSync(`node ${VALIDATOR_SCRIPT} protocol ${PROTOCOL_FILE}`, { encoding: 'utf8' });
            expect(output).toContain('valid');
        } catch (error) {
            console.error(error.stdout);
            throw error;
        }
    });

    it('should validate the discovery example', () => {
        const exampleFile = path.join(__dirname, '..', 'examples', 'discovery_output.json');
        if (fs.existsSync(exampleFile)) {
            try {
                const output = execSync(`node ${VALIDATOR_SCRIPT} output ${exampleFile} discovery`, { encoding: 'utf8' });
                expect(output).toContain('valid');
            } catch (error) {
                console.error(error.stdout);
                throw error;
            }
        }
    });
});
