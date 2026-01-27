const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PROTOCOL_FILE = path.join(__dirname, '..', 'rup-protocol.yaml');
const VALIDATOR_SCRIPT = path.join(__dirname, '..', 'validators', 'validate_rup.js');

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
            expect(output.toLowerCase()).toContain('valid');
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
                expect(output.toLowerCase()).toContain('valid');
            } catch (error) {
                console.error(error.stdout);
                throw error;
            }
        }
    });

    it('should reject excessive YAML aliases (billion laughs defense)', () => {
        const tmpFile = path.join(__dirname, 'alias_bomb.yaml');
        const lines = ['a0: &a0 lol'];
        for (let i = 1; i < 20; i += 1) {
            lines.push(`a${i}: *a0`);
        }
        fs.writeFileSync(tmpFile, lines.join('\n') + '\n');

        try {
            execSync(`node ${VALIDATOR_SCRIPT} protocol ${tmpFile}`, {
                encoding: 'utf8',
                env: { ...process.env, RUP_MAX_YAML_ALIASES: '5' },
                stdio: 'pipe',
            });
            throw new Error('Expected validation to fail due to alias limit');
        } catch (error) {
            // Expected to fail
            expect(error.status).toBe(1);
        } finally {
            fs.unlinkSync(tmpFile);
        }
    });
});
