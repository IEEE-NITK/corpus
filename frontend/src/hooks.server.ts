import winston from "winston";
import { inspect } from "util";

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    defaultMeta: { service: 'corpus-frontend' },
    transports: [
        new winston.transports.Console({ format: winston.format.simple() }), // Has to be changed to file once log monitoring is enabled.
    ],
});

export async function handle({ event, resolve }) {
    const response = await resolve(event);
    logger.info(inspect(event));
    return response;
}
