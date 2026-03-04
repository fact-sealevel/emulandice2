FROM rocker/tidyverse:4.5.1

RUN apt update && apt install -y cmake libnetcdf-dev && apt clean

# RUN R -e "install.packages('renv', version='1.1.5')"
# RUN R -e "renv::init(bare=TRUE)"
# RUN R -e "renv::install('tamsinedwards/emulandice2@fd3190')"
# RUN R -e "renv::snapshot(type='all')"

# Create an environment for R based on an renv lock of all dependencies.
COPY renv.lock renv.lock
RUN R -q --no-save -e "install.packages('renv', version='1.1.5')"
RUN R -q --no-save -e "renv::restore()"

COPY --from=ghcr.io/astral-sh/uv:0.9.6 /uv /uvx /bin/

# Where we're installing this thing.
ARG APP_HOME="/opt/emulandice2"

# Use custom user/group so container not run with root permissions.
USER 9876:9876

WORKDIR ${APP_HOME}

COPY . .

# Set HOME so uv installs python here, where it has permissions.
ENV HOME=${APP_HOME}
# Install the application dependencies into a local virtual environment, compiling to bytecode.
RUN uv sync --frozen --no-cache --no-dev --compile-bytecode

# Easily run commands from the environment just created.
ENV PATH="${APP_HOME}/.venv/bin:$PATH"

# So CLI app knows where to find the magic R script to run emulandice2
ENV EMULANDICE2_R_SCRIPT_PATH="${APP_HOME}/scripts/main.R"

# Keep Python from buffering output to stdout, stderror.
# Prevents mangling or out of order write with R subprocess print messages.
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["emulandice2"]
